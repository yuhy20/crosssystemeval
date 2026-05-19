"""Re-run a single failed judge cell and splice the result back into the raw
output file. Used to recover from transient rate-limit failures.

Usage:
    cd code/trident_repro
    uv run python scripts/rerun_judge_cell.py \
        --rubric doctor --judge gpt-4o --response-idx 22
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PKG_SRC = SCRIPT_DIR.parent / "src"
if str(PKG_SRC) not in sys.path:
    sys.path.insert(0, str(PKG_SRC))

from trident_repro.config import configure_logging, get_settings  # noqa: E402
from trident_repro.models import build_client  # noqa: E402

from rubric_data import RUBRIC_CONFIG  # noqa: E402
from run_llm_judge import JUDGE_SYSTEM, parse_judge_output  # noqa: E402
from run_llm_judge_role import (  # noqa: E402
    PILOT_DIR,
    RESPONSES_PATH,
    build_judge_user_message,
)

logger = logging.getLogger("crosssystemeval.rerun_judge")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rubric", required=True, choices=sorted(RUBRIC_CONFIG.keys()))
    parser.add_argument("--judge", required=True)
    parser.add_argument("--response-idx", type=int, required=True)
    args = parser.parse_args()

    configure_logging("INFO")
    cfg = RUBRIC_CONFIG[args.rubric]
    raw_path = PILOT_DIR / cfg["output"]

    # Load existing raw rows.
    rows = [json.loads(line) for line in raw_path.read_text().splitlines() if line.strip()]
    target_idx = None
    for i, r in enumerate(rows):
        if r["judge_model"] == args.judge and r["response_idx"] == args.response_idx:
            target_idx = i
            break
    if target_idx is None:
        logger.error("no row found for judge=%s response_idx=%d", args.judge, args.response_idx)
        return 1
    target = rows[target_idx]
    logger.info("found row %d, prior error: %s", target_idx, (target.get("error") or "")[:120])

    # Load the response text.
    responses = [json.loads(line) for line in RESPONSES_PATH.read_text().splitlines() if line.strip()]
    response_row = responses[args.response_idx]
    assert response_row["model"] == target["response_model"]
    assert response_row["prompt_id"] == target["prompt_id"]

    # Preserve the original item_order (randomization seed already burned).
    item_order = target["item_order"]
    user_msg = build_judge_user_message(
        rubric_items=cfg["items"],
        response_text=response_row["response"],
        item_order=item_order,
    )

    settings = get_settings()
    client = build_client(
        args.judge,
        anthropic_key=settings.optional_anthropic_key(),
        openai_key=settings.optional_openai_key(),
        groq_key=settings.optional_groq_key(),
    )

    started = _now()
    logger.info("re-judging idx=%d judge=%s rubric=%s", args.response_idx, args.judge, args.rubric)
    raw = client.complete(
        system=JUDGE_SYSTEM,
        user=user_msg,
        max_tokens=2500,
        temperature=0.0,
    )
    parsed = parse_judge_output(raw)
    finished = _now()
    err = None if parsed is not None else "parse_failed"

    rows[target_idx] = {
        **target,
        "raw_output": raw,
        "parsed_scores": parsed,
        "error": err,
        "started_at": started,
        "finished_at": finished,
    }
    with raw_path.open("w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    logger.info("wrote %d rows; rerun status: %s", len(rows), "ok" if parsed else "still_failed")
    return 0 if parsed else 2


if __name__ == "__main__":
    raise SystemExit(main())
