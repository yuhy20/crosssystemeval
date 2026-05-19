"""LLM-as-judge pipeline — role-specific source-first rubric (lawyer / doctor).

Mirrors `run_llm_judge.py` but takes a `--rubric` argument and scores only the
responses whose framing is in the rubric's framing-filter set (baseline +
target role), so we get clean delta-from-baseline ICR per the rubric.

Output: data/pilot/judge_v2/llm_judge_{rubric}_raw.jsonl

Usage:
    cd code/trident_repro
    uv run python scripts/run_llm_judge_role.py --rubric lawyer
    uv run python scripts/run_llm_judge_role.py --rubric doctor
"""

from __future__ import annotations

import argparse
import json
import logging
import random
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

from rubric_data import RUBRIC_CONFIG  # noqa: E402
from run_crosssystemeval_pilot import SHARED_SCENARIO  # noqa: E402
from run_llm_judge import (  # noqa: E402
    JUDGE_MODELS,
    JUDGE_SYSTEM,
    parse_judge_output,
)

logger = logging.getLogger("crosssystemeval.llm_judge_role")

REPO_ROOT = SCRIPT_DIR.resolve().parents[2]
PILOT_DIR = REPO_ROOT / "data" / "pilot" / "judge_v2"
RESPONSES_PATH = PILOT_DIR / "responses.jsonl"


def _format_item_for_prompt(item: dict) -> str:
    quote_line = f"*Source clause (verbatim):* {item['quote']}\n" if item.get("quote") else ""
    return (
        f"### Item {item['n']}. {item['title']}\n"
        f"*Source:* {item['source']}\n"
        f"{quote_line}"
        f"- 0 — {item['anchors'][0]}\n"
        f"- 1 — {item['anchors'][1]}\n"
        f"- 2 — {item['anchors'][2]}\n"
        f"- 3 — {item['anchors'][3]}\n"
    )


def build_judge_user_message(
    *,
    rubric_items: list[dict],
    response_text: str,
    item_order: list[int],
) -> str:
    items_by_n = {item["n"]: item for item in rubric_items}
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
        "matter above. The user's framing (baseline vs. a role claim) is "
        "HIDDEN from you so the score reflects the response on its merits "
        "against the rubric below.\n\n"
        "```\n"
        f"{response_text}\n"
        "```\n\n"
        "---\n\n"
        "# Rubric items (items presented in randomized order — score each "
        "independently against the controlling rule text)\n\n"
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
    rubric_items: list[dict],
    judge_models: list[str],
    responses: list[dict],
    seed: int = 20260518,
) -> list[JudgeCall]:
    settings = get_settings()
    anthropic_key = settings.optional_anthropic_key()
    openai_key = settings.optional_openai_key()
    groq_key = settings.optional_groq_key()

    item_numbers = sorted(item["n"] for item in rubric_items)
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
                rubric_items=rubric_items,
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
                    max_tokens=2500,
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


def filter_responses_for_rubric(
    responses: list[dict], framings: set[str]
) -> list[tuple[int, dict]]:
    """Return (original_index, row) tuples for rows whose framing matches.

    Preserving the original index keeps response_idx interpretable against
    the canonical responses.jsonl ordering.
    """
    return [
        (idx, row)
        for idx, row in enumerate(responses)
        if row.get("framing") in framings
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--rubric",
        required=True,
        choices=sorted(RUBRIC_CONFIG.keys()),
        help="Which role-rubric to run (lawyer or doctor).",
    )
    args = parser.parse_args()
    cfg = RUBRIC_CONFIG[args.rubric]

    configure_logging("INFO")
    responses = load_responses()
    logger.info("loaded %d responses from %s", len(responses), RESPONSES_PATH)

    filtered = filter_responses_for_rubric(responses, cfg["framings"])
    logger.info(
        "rubric=%s framings=%s filtered=%d / %d responses",
        args.rubric,
        sorted(cfg["framings"]),
        len(filtered),
        len(responses),
    )
    logger.info("judges: %s", ", ".join(JUDGE_MODELS))

    # We pass the filtered responses to run_judging, but stamp response_idx
    # with the original index so analysis can join back to responses.jsonl.
    filtered_rows = [row for _, row in filtered]
    original_indices = [idx for idx, _ in filtered]

    calls = run_judging(
        rubric_items=cfg["items"],
        judge_models=JUDGE_MODELS,
        responses=filtered_rows,
    )

    # Remap response_idx from filtered-position to original-position.
    n_filtered = len(filtered_rows)
    for c in calls:
        if c.response_idx < n_filtered:
            c.response_idx = original_indices[c.response_idx]

    out_path = PILOT_DIR / cfg["output"]
    with out_path.open("w") as f:
        for c in calls:
            f.write(json.dumps(_to_record(c), ensure_ascii=False) + "\n")
    logger.info("wrote %d judge calls to %s", len(calls), out_path)

    n_ok = sum(1 for c in calls if c.parsed_scores is not None)
    n_err = sum(1 for c in calls if c.error)
    logger.info("rubric=%s summary: ok=%d err=%d", args.rubric, n_ok, n_err)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
