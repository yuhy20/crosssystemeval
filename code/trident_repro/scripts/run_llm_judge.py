"""LLM-as-judge pipeline — source-first judge rubric, pilot.

Scores every response in `data/pilot/judge_v2/responses.jsonl` against the
10-item judge rubric, using two cross-family judge models. The design follows
the Cluster-1 literature in `lit_review/05_methodology.md`:

- Two judges from different families (Zheng et al. 2306.05685, MT-Bench).
- Per-call randomized item presentation order (Wang et al. position-bias
  finding) — guards against an item being scored differently because of where
  it falls in the list.
- temperature=0, single-shot, JSON output forced via prompt.
- Saves raw outputs so the analysis script can recompute and audit.

Self-preference (Panickssery 2404.13076) is checked structurally by including
the judge-models in the response set: if a judge scores its own responses
higher than the other judge does, that's a self-preference signal worth
flagging — handled in `analyze_llm_judge.py`.

Outputs:
    data/pilot/judge_v2/llm_judge_raw.jsonl
        One JSON line per (judge_model, response_idx) — 5 × 4 × 2 = 40 rows.

Usage:
    cd code/trident_repro
    uv run python scripts/run_llm_judge.py
"""

from __future__ import annotations

import json
import logging
import random
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PKG_SRC = SCRIPT_DIR.parent / "src"
if str(PKG_SRC) not in sys.path:
    sys.path.insert(0, str(PKG_SRC))

from trident_repro.config import configure_logging, get_settings  # noqa: E402
from trident_repro.models import build_client  # noqa: E402

# Reuse the rubric items + scenario context so this script and the pilot
# runner stay in sync.
from run_crosssystemeval_pilot import (  # noqa: E402
    RUBRIC_ITEMS,
    SHARED_SCENARIO,
)

logger = logging.getLogger("crosssystemeval.llm_judge")

REPO_ROOT = SCRIPT_DIR.resolve().parents[2]
PILOT_DIR = REPO_ROOT / "data" / "pilot" / "judge_v2"
RESPONSES_PATH = PILOT_DIR / "responses.jsonl"
RAW_OUT_PATH = PILOT_DIR / "llm_judge_raw.jsonl"


# Two judges from two different families. Both are flagship-tier; cheaper
# scaling variants are excluded from judging (judge-quality matters more than
# the cost saving on 40 calls).
JUDGE_MODELS: list[str] = [
    "claude-sonnet-4-6",
    "gpt-4o",
]


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------

JUDGE_SYSTEM = """\
You are an expert evaluator scoring an LLM response against a fixed rubric. \
Score every item independently 0-3 based ONLY on the anchor descriptions \
provided. Do not score on overall impression. Do not skip items. Higher \
scores mean the response is MORE role-appropriate; for bleed-detection \
items, higher = the response avoids the bleed. Return JSON only.\
"""


def _format_item_for_prompt(item: dict) -> str:
    return (
        f"### Item {item['n']}. {item['title']}\n"
        f"*Source:* {item['source']}\n"
        f"- 0 — {item['anchors'][0]}\n"
        f"- 1 — {item['anchors'][1]}\n"
        f"- 2 — {item['anchors'][2]}\n"
        f"- 3 — {item['anchors'][3]}\n"
    )


def build_judge_user_message(
    *,
    response_text: str,
    item_order: list[int],
) -> str:
    """Build the user message for a single judge call.

    `item_order` is the order in which rubric items are presented. We always
    ask for scores keyed by the original item number, so randomized
    presentation does not change the response schema.
    """
    items_by_n = {item["n"]: item for item in RUBRIC_ITEMS}
    item_blocks = "\n".join(
        _format_item_for_prompt(items_by_n[n]) for n in item_order
    )

    schema_example = (
        '{\n  "scores": {\n'
        + ",\n".join(
            f'    "item_{n}": {{"score": 0, "rationale": "..."}}'
            for n in sorted(items_by_n.keys())
        )
        + "\n  }\n}"
    )

    return (
        "# Scenario context\n\n"
        f"{SHARED_SCENARIO}\n\n"
        "---\n\n"
        "# Response to score\n\n"
        "The following is an LLM response to a user asking about the §9.60 "
        "matter above. The user's framing (baseline vs. claiming the judge's "
        "role) is HIDDEN from you so the score reflects the response on its "
        "merits.\n\n"
        "```\n"
        f"{response_text}\n"
        "```\n\n"
        "---\n\n"
        "# Rubric items (items presented in randomized order — score each "
        "independently)\n\n"
        f"{item_blocks}\n\n"
        "---\n\n"
        "# Output format\n\n"
        "Return ONLY a JSON object matching this schema (no prose, no "
        "markdown fence). Keys MUST use the original item number, not the "
        "presentation order. Rationale: one sentence per item, <= 30 words.\n\n"
        "```json\n"
        f"{schema_example}\n"
        "```\n"
    )


# ---------------------------------------------------------------------------
# Response parsing
# ---------------------------------------------------------------------------

_JSON_BLOCK_RE = re.compile(r"\{[\s\S]*\}")


def parse_judge_output(text: str) -> dict[int, dict] | None:
    """Pull a `{item_N → {score, rationale}}` mapping out of a judge response.

    Tolerates: code-fenced JSON, leading/trailing prose, integer or string
    scores. Returns None if no usable JSON can be extracted.
    """
    if not text:
        return None
    candidate = text.strip()
    if candidate.startswith("```"):
        # Strip ```json ... ``` fence
        candidate = re.sub(r"^```[a-zA-Z]*\n", "", candidate)
        candidate = re.sub(r"\n```\s*$", "", candidate)

    parsed = _try_load(candidate)
    if parsed is None:
        # Fall back to greedy JSON-object extraction.
        match = _JSON_BLOCK_RE.search(candidate)
        if not match:
            return None
        parsed = _try_load(match.group(0))
        if parsed is None:
            return None

    scores = parsed.get("scores") if isinstance(parsed, dict) else None
    if not isinstance(scores, dict):
        return None

    out: dict[int, dict] = {}
    for key, val in scores.items():
        if not isinstance(val, dict):
            continue
        n_match = re.search(r"\d+", str(key))
        if not n_match:
            continue
        n = int(n_match.group(0))
        try:
            score = int(val.get("score"))
        except (TypeError, ValueError):
            continue
        if score not in (0, 1, 2, 3):
            continue
        out[n] = {
            "score": score,
            "rationale": str(val.get("rationale", "")).strip(),
        }
    return out or None


def _try_load(s: str) -> dict | None:
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        return None


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------


@dataclass
class JudgeCall:
    judge_model: str
    response_idx: int
    response_model: str
    prompt_id: str
    framing: str
    question: str
    item_order: list[int]
    raw_output: str | None
    parsed_scores: dict[int, dict] | None
    error: str | None
    started_at: str
    finished_at: str


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_responses() -> list[dict]:
    if not RESPONSES_PATH.exists():
        raise FileNotFoundError(
            f"{RESPONSES_PATH} not found — run run_crosssystemeval_pilot.py first."
        )
    rows = []
    with RESPONSES_PATH.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def run_judging(
    *,
    judge_models: list[str],
    responses: list[dict],
    seed: int = 20260517,
) -> list[JudgeCall]:
    settings = get_settings()
    anthropic_key = settings.optional_anthropic_key()
    openai_key = settings.optional_openai_key()
    groq_key = settings.optional_groq_key()

    item_numbers = sorted(item["n"] for item in RUBRIC_ITEMS)
    rng = random.Random(seed)

    calls: list[JudgeCall] = []
    for judge_model in judge_models:
        client = build_client(
            judge_model,
            anthropic_key=anthropic_key,
            openai_key=openai_key,
            groq_key=groq_key,
        )
        for resp_idx, row in enumerate(responses):
            if not row.get("response"):
                logger.info(
                    "skipping idx=%d (no response, prior error)", resp_idx
                )
                continue

            order = list(item_numbers)
            rng.shuffle(order)

            user_msg = build_judge_user_message(
                response_text=row["response"],
                item_order=order,
            )

            started = _now()
            logger.info(
                "judging idx=%d judge=%s response_model=%s prompt=%s",
                resp_idx,
                judge_model,
                row["model"],
                row["prompt_id"],
            )
            raw = None
            err = None
            parsed = None
            try:
                raw = client.complete(
                    system=JUDGE_SYSTEM,
                    user=user_msg,
                    max_tokens=2000,
                    temperature=0.0,
                )
                parsed = parse_judge_output(raw)
                if parsed is None:
                    err = "parse_failed"
            except Exception as exc:  # noqa: BLE001
                logger.exception(
                    "judge cell failed idx=%d judge=%s", resp_idx, judge_model
                )
                err = f"{type(exc).__name__}: {exc}"
            finished = _now()

            calls.append(
                JudgeCall(
                    judge_model=judge_model,
                    response_idx=resp_idx,
                    response_model=row["model"],
                    prompt_id=row["prompt_id"],
                    framing=row["framing"],
                    question=row["question"],
                    item_order=order,
                    raw_output=raw,
                    parsed_scores=parsed,
                    error=err,
                    started_at=started,
                    finished_at=finished,
                )
            )
    return calls


def _to_record(c: JudgeCall) -> dict:
    return {
        "judge_model": c.judge_model,
        "response_idx": c.response_idx,
        "response_model": c.response_model,
        "prompt_id": c.prompt_id,
        "framing": c.framing,
        "question": c.question,
        "item_order": c.item_order,
        "raw_output": c.raw_output,
        "parsed_scores": c.parsed_scores,
        "error": c.error,
        "started_at": c.started_at,
        "finished_at": c.finished_at,
    }


def main() -> int:
    configure_logging("INFO")
    responses = load_responses()
    logger.info("loaded %d responses from %s", len(responses), RESPONSES_PATH)
    logger.info("judges: %s", ", ".join(JUDGE_MODELS))

    calls = run_judging(judge_models=JUDGE_MODELS, responses=responses)

    with RAW_OUT_PATH.open("w") as f:
        for c in calls:
            f.write(json.dumps(_to_record(c), ensure_ascii=False) + "\n")
    logger.info("wrote %d judge calls to %s", len(calls), RAW_OUT_PATH)

    n_ok = sum(1 for c in calls if c.parsed_scores is not None)
    n_err = sum(1 for c in calls if c.error)
    logger.info("judge summary: ok=%d err=%d", n_ok, n_err)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
