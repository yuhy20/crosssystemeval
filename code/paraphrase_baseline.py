"""Paraphrase-stability baseline for the source-first judge rubric.

Goal
----
Distinguish *content-sensitive* rubric items (scores stay stable when the
response is paraphrased) from *wording-sensitive* ones (scores swing under
paraphrase). A well-calibrated rubric — anchored to verbatim codified text
per `rubrics/judge_v2_source_first.md` — should be largely paraphrase-stable.
Items whose scores swing significantly under paraphrase are flagged for
review: their anchors may be cuing on surface lexical features
(e.g., presence of the literal token "§9.60(c)") rather than substantive
legal content (e.g., engaging the criteria-issuance test).

Pipeline
--------
For each response in `data/pilot/judge_v2/responses.jsonl`:
  1. Paraphrase the response once via an LLM with a meaning-preserving prompt
     (different surface form, same legal substance, same citations).
  2. Re-score the paraphrase under the same rubric, with the same two cross-
     family judges used in `run_llm_judge.py` (`claude-sonnet-4-6`, `gpt-4o`),
     using the same prompt scaffolding and item-order randomization.
  3. For each (response_idx, judge_model, item_n) cell, record:
        original_score   — from llm_judge_raw.jsonl
        paraphrased_score — from this run
        delta             — paraphrased − original
  4. Aggregate per-item mean |delta| and write a summary md.

Outputs
-------
    data/pilot/judge_v2/paraphrase_baseline.jsonl
        One row per (judge_model, response_idx) with original_score map,
        paraphrased_score map, per-item delta map, and the paraphrased text.
    data/pilot/judge_v2/paraphrase_baseline.md
        Human-readable summary: per-item mean |delta|, mean delta, and a
        flag for items whose mean |delta| exceeds the stability threshold.

CLI
---
    python code/paraphrase_baseline.py \
        --responses data/pilot/judge_v2/responses.jsonl \
        --rubric rubrics/judge_v2_source_first.md \
        --output-dir data/pilot/judge_v2

    Optional flags:
      --paraphrase-model  (default: claude-sonnet-4-6)
      --judges            (comma-sep; default: claude-sonnet-4-6,gpt-4o)
      --raw-judge-path    (default: <output-dir>/llm_judge_raw.jsonl)
      --seed              (default: 20260518)
      --dry-run           Build paraphrase prompts and judge prompts, but do
                          NOT call any API. Writes the planned-call manifest
                          to <output-dir>/paraphrase_baseline_dryrun.jsonl
                          so the harness can be validated without API spend.

Dependencies discovered
-----------------------
- The repo's LLM-client and judge-pipeline live in `code/trident_repro/`,
  not at the top-level `code/` paths named in the task spec. We re-use:
    - trident_repro.models.build_client       (chat-client factory)
    - trident_repro.config.{configure_logging, get_settings}
    - scripts.run_llm_judge.{JUDGE_SYSTEM,
                             build_judge_user_message,
                             parse_judge_output}
    - scripts.run_crosssystemeval_pilot.{RUBRIC_ITEMS, SHARED_SCENARIO}
  These imports keep judging logic identical to the pilot run, so any score
  delta is attributable to the paraphrase, not to scaffolding drift.

Notes
-----
- We do NOT regenerate original scores. We read them from
  `llm_judge_raw.jsonl` (40 rows) so paraphrase-only is the active variable.
- The paraphrase model defaults to `claude-sonnet-4-6` for stability; using
  a model from the same family as one of the judges is intentional — a
  paraphrase that loses substantive content should drop the score even from
  the same-family judge.
- This script is documented and CLI-wired but NOT executed in this commit:
  no API spend has been incurred. Use `--dry-run` to validate plumbing.
"""

from __future__ import annotations

import argparse
import json
import logging
import random
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# --- Repo path bootstrapping -------------------------------------------------
# code/paraphrase_baseline.py is at <repo>/code/. The reusable harness lives
# at <repo>/code/trident_repro/src and <repo>/code/trident_repro/scripts.
SCRIPT_DIR = Path(__file__).resolve().parent  # <repo>/code
REPO_ROOT = SCRIPT_DIR.parent
TRIDENT_DIR = SCRIPT_DIR / "trident_repro"
TRIDENT_SRC = TRIDENT_DIR / "src"
TRIDENT_SCRIPTS = TRIDENT_DIR / "scripts"
for p in (TRIDENT_SRC, TRIDENT_SCRIPTS):
    if p.exists() and str(p) not in sys.path:
        sys.path.insert(0, str(p))

try:
    from trident_repro.config import configure_logging, get_settings  # type: ignore  # noqa: E402
    from trident_repro.models import build_client  # type: ignore  # noqa: E402

    # The judge prompt scaffolding + parser are defined in the existing
    # pilot judge script. Reusing them keeps the paraphrased-response
    # scoring identical to the original scoring up to the response text.
    from run_llm_judge import (  # type: ignore  # noqa: E402
        JUDGE_SYSTEM,
        build_judge_user_message,
        parse_judge_output,
    )
    from run_crosssystemeval_pilot import (  # type: ignore  # noqa: E402
        RUBRIC_ITEMS,
        SHARED_SCENARIO,
    )

    _IMPORTS_OK = True
    _IMPORT_ERROR: str | None = None
except Exception as _exc:  # noqa: BLE001
    # If trident_repro isn't installed/available, fall back to documenting
    # the expected interface so the harness still imports cleanly for code
    # review. Actual execution will fail with a clear message.
    _IMPORTS_OK = False
    _IMPORT_ERROR = f"{type(_exc).__name__}: {_exc}"

logger = logging.getLogger("crosssystemeval.paraphrase_baseline")


# ---------------------------------------------------------------------------
# Expected LLM client interface
# ---------------------------------------------------------------------------
# The chat client used here is `trident_repro.models.ChatClient`, a runtime-
# checkable Protocol with:
#
#     class ChatClient(Protocol):
#         model: str
#         def complete(
#             self, *, system: str, user: str,
#             max_tokens: int = 1024, temperature: float = 0.0,
#         ) -> str: ...
#
# If the trident_repro package is unavailable, swap `_get_client` for any
# callable returning an object that satisfies the same Protocol.
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Paraphrase prompt
# ---------------------------------------------------------------------------

PARAPHRASE_SYSTEM = """\
You are a careful editor. Your job is to paraphrase a legal-analysis \
response so that the surface wording changes substantially while the \
substantive content is preserved exactly. Preserve every: statutory \
citation (e.g., §9.60(c), §9.60(j)(3)), case citation, rule number \
(e.g., Rule 2.9(C)), factual reference to the underlying scenario, and \
every legal conclusion. Do NOT add new analysis, do NOT remove analysis, \
do NOT change the order of substantive claims. Vary sentence structure, \
section headings, and word choice. Return ONLY the paraphrased response \
text with no preamble.\
"""


def build_paraphrase_user_message(response_text: str) -> str:
    """Build the user message for a paraphrase call."""
    return (
        "# Scenario context (for reference; do not paraphrase this block)\n\n"
        f"{SHARED_SCENARIO}\n\n"
        "---\n\n"
        "# Response to paraphrase\n\n"
        "Rewrite the following response with substantially different surface "
        "wording but identical substantive legal content. Preserve every "
        "citation and every conclusion verbatim where citations are involved.\n\n"
        "```\n"
        f"{response_text}\n"
        "```\n\n"
        "---\n\n"
        "Return ONLY the paraphrased text. No explanation, no preamble."
    )


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class OriginalScores:
    """Original judge scores loaded from llm_judge_raw.jsonl.

    Indexed by (judge_model, response_idx) → {item_n: score}.
    """

    by_cell: dict[tuple[str, int], dict[int, int]] = field(default_factory=dict)

    def get(self, judge_model: str, response_idx: int) -> dict[int, int]:
        return self.by_cell.get((judge_model, response_idx), {})


@dataclass
class ParaphraseCell:
    judge_model: str
    response_idx: int
    response_model: str
    prompt_id: str
    framing: str
    paraphrase_model: str
    item_order: list[int]
    paraphrased_text: str | None
    original_scores: dict[int, int]
    paraphrased_scores: dict[int, int] | None
    deltas: dict[int, int] | None
    raw_judge_output: str | None
    error: str | None
    started_at: str
    finished_at: str

    def to_record(self) -> dict[str, Any]:
        return {
            "judge_model": self.judge_model,
            "response_idx": self.response_idx,
            "response_model": self.response_model,
            "prompt_id": self.prompt_id,
            "framing": self.framing,
            "paraphrase_model": self.paraphrase_model,
            "item_order": self.item_order,
            "paraphrased_text": self.paraphrased_text,
            "original_scores": self.original_scores,
            "paraphrased_scores": self.paraphrased_scores,
            "deltas": self.deltas,
            "raw_judge_output": self.raw_judge_output,
            "error": self.error,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
        }


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ---------------------------------------------------------------------------
# IO
# ---------------------------------------------------------------------------


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def load_original_scores(raw_judge_path: Path) -> OriginalScores:
    """Pull (judge_model, response_idx) → {item_n: score} from llm_judge_raw.jsonl."""
    if not raw_judge_path.exists():
        raise FileNotFoundError(
            f"{raw_judge_path} not found — run scripts/run_llm_judge.py first."
        )
    out = OriginalScores()
    for row in load_jsonl(raw_judge_path):
        parsed = row.get("parsed_scores") or {}
        # parsed_scores may be keyed by int or str depending on JSON round-trip.
        score_map: dict[int, int] = {}
        for k, v in parsed.items():
            try:
                n = int(k)
            except (TypeError, ValueError):
                continue
            if not isinstance(v, dict):
                continue
            s = v.get("score")
            if isinstance(s, int) and s in (0, 1, 2, 3):
                score_map[n] = s
        if score_map:
            out.by_cell[(row["judge_model"], int(row["response_idx"]))] = score_map
    return out


# ---------------------------------------------------------------------------
# Paraphrase + re-judge
# ---------------------------------------------------------------------------


def _get_client(model: str):
    """Build a ChatClient for the given model id (delegates to trident_repro)."""
    if not _IMPORTS_OK:
        # TODO: If `trident_repro` is removed, replace this with a direct
        # client construction:
        #
        #   import anthropic, openai
        #   if model.startswith("claude"):
        #       return AnthropicChatClient(api_key=..., model=model)
        #   else:
        #       return OpenAIChatClient(api_key=..., model=model)
        #
        # See trident_repro/models.py for the canonical implementation that
        # this harness expects (ChatClient Protocol with `.complete(system=,
        # user=, max_tokens=, temperature=) -> str`).
        raise RuntimeError(
            "trident_repro package not importable: "
            f"{_IMPORT_ERROR}. Re-enable imports or stub _get_client."
        )
    settings = get_settings()
    return build_client(
        model,
        anthropic_key=settings.optional_anthropic_key(),
        openai_key=settings.optional_openai_key(),
        groq_key=settings.optional_groq_key(),
    )


def paraphrase_response(
    *,
    response_text: str,
    paraphrase_client,
    max_tokens: int = 4000,
) -> str:
    """Single paraphrase call. temperature=0.2 for some surface variety."""
    return paraphrase_client.complete(
        system=PARAPHRASE_SYSTEM,
        user=build_paraphrase_user_message(response_text),
        max_tokens=max_tokens,
        temperature=0.2,
    )


def score_paraphrase(
    *,
    paraphrased_text: str,
    judge_client,
    item_order: list[int],
) -> tuple[str, dict[int, int] | None]:
    """Re-invoke the judge pipeline on the paraphrased text.

    Returns (raw_output, parsed_score_map).
    """
    user_msg = build_judge_user_message(
        response_text=paraphrased_text,
        item_order=item_order,
    )
    raw = judge_client.complete(
        system=JUDGE_SYSTEM,
        user=user_msg,
        max_tokens=2000,
        temperature=0.0,
    )
    parsed = parse_judge_output(raw)
    if parsed is None:
        return raw, None
    return raw, {n: v["score"] for n, v in parsed.items()}


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------


def _compute_deltas(
    original: dict[int, int], paraphrased: dict[int, int]
) -> dict[int, int]:
    return {
        n: paraphrased[n] - original[n]
        for n in sorted(set(original) & set(paraphrased))
    }


def run_paraphrase_baseline(
    *,
    responses: list[dict],
    original_scores: OriginalScores,
    judges: list[str],
    paraphrase_model: str,
    seed: int,
    dry_run: bool,
) -> list[ParaphraseCell]:
    item_numbers = sorted(item["n"] for item in RUBRIC_ITEMS)
    rng = random.Random(seed)

    paraphrase_client = None if dry_run else _get_client(paraphrase_model)
    judge_clients = {} if dry_run else {jm: _get_client(jm) for jm in judges}

    cells: list[ParaphraseCell] = []
    # Paraphrase once per response (not per judge): the paraphrased text is
    # the input variable; scoring it across judges measures cross-judge
    # stability on the paraphrase, not paraphrase variance.
    paraphrase_cache: dict[int, str] = {}

    for resp_idx, row in enumerate(responses):
        if not row.get("response"):
            logger.info("skipping idx=%d (no response)", resp_idx)
            continue

        # 1) Paraphrase the response (once).
        started = _now()
        paraphrased_text: str | None = paraphrase_cache.get(resp_idx)
        paraphrase_err: str | None = None
        if paraphrased_text is None:
            if dry_run:
                paraphrased_text = "[DRY RUN — paraphrase not executed]"
            else:
                try:
                    logger.info(
                        "paraphrasing idx=%d model=%s prompt=%s",
                        resp_idx,
                        paraphrase_model,
                        row["prompt_id"],
                    )
                    paraphrased_text = paraphrase_response(
                        response_text=row["response"],
                        paraphrase_client=paraphrase_client,
                    )
                except Exception as exc:  # noqa: BLE001
                    paraphrase_err = f"paraphrase_failed: {type(exc).__name__}: {exc}"
                    logger.exception("paraphrase failed idx=%d", resp_idx)
            if paraphrased_text is not None:
                paraphrase_cache[resp_idx] = paraphrased_text

        # 2) Score the paraphrase under each judge.
        for judge_model in judges:
            order = list(item_numbers)
            rng.shuffle(order)

            originals = original_scores.get(judge_model, resp_idx)
            if not originals:
                logger.warning(
                    "no original scores for judge=%s idx=%d — skipping cell",
                    judge_model,
                    resp_idx,
                )
                continue

            raw_judge_output: str | None = None
            paraphrased_scores: dict[int, int] | None = None
            err: str | None = paraphrase_err

            if paraphrased_text is not None and err is None:
                if dry_run:
                    raw_judge_output = "[DRY RUN — judge not invoked]"
                else:
                    try:
                        raw_judge_output, paraphrased_scores = score_paraphrase(
                            paraphrased_text=paraphrased_text,
                            judge_client=judge_clients[judge_model],
                            item_order=order,
                        )
                        if paraphrased_scores is None:
                            err = "judge_parse_failed"
                    except Exception as exc:  # noqa: BLE001
                        err = f"judge_failed: {type(exc).__name__}: {exc}"
                        logger.exception(
                            "judge failed idx=%d judge=%s", resp_idx, judge_model
                        )

            deltas = (
                _compute_deltas(originals, paraphrased_scores)
                if paraphrased_scores is not None
                else None
            )
            finished = _now()

            cells.append(
                ParaphraseCell(
                    judge_model=judge_model,
                    response_idx=resp_idx,
                    response_model=row["model"],
                    prompt_id=row["prompt_id"],
                    framing=row["framing"],
                    paraphrase_model=paraphrase_model,
                    item_order=order,
                    paraphrased_text=paraphrased_text,
                    original_scores=originals,
                    paraphrased_scores=paraphrased_scores,
                    deltas=deltas,
                    raw_judge_output=raw_judge_output,
                    error=err,
                    started_at=started,
                    finished_at=finished,
                )
            )
    return cells


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------


def summarize(cells: list[ParaphraseCell], stability_threshold: float = 0.5) -> str:
    """Build a markdown summary of per-item paraphrase stability.

    `stability_threshold` flags items whose mean |delta| (averaged across
    cells with a successfully parsed delta) exceeds this value. 0.5 is a
    conservative starting cut: on a 0-3 scale, a mean |delta| > 0.5 means
    the item routinely swings by half a level under paraphrase.
    """
    item_titles = {item["n"]: item["title"] for item in RUBRIC_ITEMS}
    abs_deltas: dict[int, list[int]] = {n: [] for n in item_titles}
    signed_deltas: dict[int, list[int]] = {n: [] for n in item_titles}

    n_cells = 0
    n_cells_ok = 0
    for c in cells:
        n_cells += 1
        if c.deltas is None:
            continue
        n_cells_ok += 1
        for n, d in c.deltas.items():
            abs_deltas.setdefault(n, []).append(abs(d))
            signed_deltas.setdefault(n, []).append(d)

    def _mean(xs: list[int]) -> float:
        return sum(xs) / len(xs) if xs else 0.0

    lines: list[str] = []
    lines.append("# Paraphrase-stability baseline — summary\n")
    lines.append(
        f"- Cells total: {n_cells} (judge × response). "
        f"Cells with usable delta: {n_cells_ok}.\n"
    )
    lines.append(
        "- Per-item mean |delta| measures paraphrase sensitivity on a 0-3 "
        f"scale. Items with mean |delta| > {stability_threshold:.2f} are "
        "flagged for review (content-sensitive rubrics should have low |delta|).\n"
    )
    lines.append("\n| Item | Title | n | mean Δ | mean |Δ| | flag |\n")
    lines.append("|---:|---|---:|---:|---:|:---|\n")

    flagged: list[int] = []
    for n in sorted(item_titles):
        xs_abs = abs_deltas.get(n, [])
        xs_signed = signed_deltas.get(n, [])
        m_abs = _mean(xs_abs)
        m_signed = _mean(xs_signed)
        flag = "WORDING-SENSITIVE" if m_abs > stability_threshold else ""
        if flag:
            flagged.append(n)
        lines.append(
            f"| {n} | {item_titles[n]} | {len(xs_abs)} | "
            f"{m_signed:+.2f} | {m_abs:.2f} | {flag} |\n"
        )

    lines.append("\n## Interpretation\n")
    if flagged:
        lines.append(
            "- Flagged items "
            f"({', '.join(str(n) for n in flagged)}) showed mean |delta| above "
            f"{stability_threshold:.2f}. These anchors may be cuing on surface "
            "wording (e.g., presence of specific citation tokens) rather than "
            "the underlying substantive engagement the rubric intends to "
            "measure. Review their level-3 anchor language.\n"
        )
    else:
        lines.append(
            f"- No items exceeded the |delta| > {stability_threshold:.2f} "
            "threshold; rubric appears paraphrase-stable in this pilot.\n"
        )
    lines.append(
        "- Caveats: single paraphrase per response, 2 judges, "
        f"{n_cells_ok} usable cells — descriptive only, not inferential.\n"
    )
    return "".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else None)
    p.add_argument(
        "--responses",
        type=Path,
        default=REPO_ROOT / "data" / "pilot" / "judge_v2" / "responses.jsonl",
        help="Path to responses.jsonl (scored responses to paraphrase).",
    )
    p.add_argument(
        "--rubric",
        type=Path,
        default=REPO_ROOT / "rubrics" / "judge_v2_source_first.md",
        help=(
            "Path to the rubric markdown. Currently informational: the rubric "
            "items themselves are loaded from "
            "scripts/run_crosssystemeval_pilot.py to keep the wire format in "
            "sync with run_llm_judge.py. The path is recorded in the output "
            "header so downstream analysis knows which rubric ran."
        ),
    )
    p.add_argument(
        "--output-dir",
        type=Path,
        default=REPO_ROOT / "data" / "pilot" / "judge_v2",
        help="Directory to write paraphrase_baseline.{jsonl,md}.",
    )
    p.add_argument(
        "--paraphrase-model",
        type=str,
        default="claude-sonnet-4-6",
        help="Model id for the paraphrase generation step.",
    )
    p.add_argument(
        "--judges",
        type=str,
        default="claude-sonnet-4-6,gpt-4o",
        help="Comma-separated judge model ids (must match the original run).",
    )
    p.add_argument(
        "--raw-judge-path",
        type=Path,
        default=None,
        help=(
            "Path to llm_judge_raw.jsonl. Defaults to "
            "<output-dir>/llm_judge_raw.jsonl."
        ),
    )
    p.add_argument(
        "--seed",
        type=int,
        default=20260518,
        help="Seed for item-order randomization (matches run_llm_judge.py style).",
    )
    p.add_argument(
        "--stability-threshold",
        type=float,
        default=0.5,
        help="Mean |delta| above which an item is flagged WORDING-SENSITIVE.",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Build all paraphrase + judge prompts without calling APIs. Writes "
            "a manifest jsonl so the harness can be validated free of charge."
        ),
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    if _IMPORTS_OK:
        configure_logging("INFO")
    else:
        logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")
        logger.warning(
            "trident_repro imports failed: %s. Dry-run and summary-only modes "
            "still work; live API mode will raise.",
            _IMPORT_ERROR,
        )

    output_dir: Path = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_judge_path: Path = (
        args.raw_judge_path
        if args.raw_judge_path is not None
        else output_dir / "llm_judge_raw.jsonl"
    )
    out_jsonl = output_dir / (
        "paraphrase_baseline_dryrun.jsonl" if args.dry_run else "paraphrase_baseline.jsonl"
    )
    out_md = output_dir / "paraphrase_baseline.md"

    responses = load_jsonl(args.responses)
    logger.info("loaded %d responses from %s", len(responses), args.responses)

    original_scores = load_original_scores(raw_judge_path)
    logger.info(
        "loaded original scores for %d (judge, response) cells from %s",
        len(original_scores.by_cell),
        raw_judge_path,
    )

    judges = [j.strip() for j in args.judges.split(",") if j.strip()]
    logger.info("judges=%s paraphrase_model=%s", judges, args.paraphrase_model)
    logger.info("rubric=%s (informational; items loaded from pilot script)", args.rubric)

    cells = run_paraphrase_baseline(
        responses=responses,
        original_scores=original_scores,
        judges=judges,
        paraphrase_model=args.paraphrase_model,
        seed=args.seed,
        dry_run=args.dry_run,
    )

    with out_jsonl.open("w") as f:
        for c in cells:
            f.write(json.dumps(c.to_record(), ensure_ascii=False) + "\n")
    logger.info("wrote %d cells to %s", len(cells), out_jsonl)

    md = summarize(cells, stability_threshold=args.stability_threshold)
    with out_md.open("w") as f:
        f.write(md)
    logger.info("wrote summary to %s", out_md)

    n_ok = sum(1 for c in cells if c.deltas is not None)
    n_err = sum(1 for c in cells if c.error)
    logger.info("paraphrase-baseline summary: ok=%d err=%d", n_ok, n_err)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
