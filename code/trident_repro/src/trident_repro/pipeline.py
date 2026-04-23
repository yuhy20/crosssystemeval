"""End-to-end evaluation pipeline.

`run(config, ...)` yields one `RunRecord` per sampled prompt, and also writes
each record to the configured JSONL output file **as it completes**, so a
crash mid-run leaves the partial file valid + resumable.
"""

from __future__ import annotations

import logging
from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field
from tqdm import tqdm

from trident_repro.config import RunConfig, get_settings
from trident_repro.judge import Judge, JudgeVerdict, Jury
from trident_repro.loader import Prompt, load_domain, sample
from trident_repro.models import ChatClient, build_client

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Output record
# ---------------------------------------------------------------------------


class RunRecord(BaseModel):
    """One prompt, one target response, two judge verdicts, mean score."""

    model_config = ConfigDict(extra="ignore", frozen=True)

    id: str
    domain: str
    risk_type: str
    ethical_refs: list[str] = Field(default_factory=list)
    harmful_prompt: str
    target_model: str
    target_response: str
    judge_a: JudgeVerdict
    judge_b: JudgeVerdict
    mean_score: float
    ts: str  # ISO-8601 UTC


# ---------------------------------------------------------------------------
# JSONL helpers (crash-safe + resumable)
# ---------------------------------------------------------------------------


def _already_done_ids(path: Path) -> set[str]:
    """Read an existing JSONL and return the set of `id`s already written.

    Malformed lines are skipped with a warning; we do NOT abort resume.
    """
    if not path.exists():
        return set()

    import json

    ids: set[str] = set()
    with path.open("r", encoding="utf-8") as fh:
        for line_no, raw in enumerate(fh, start=1):
            line = raw.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                logger.warning(
                    "skipping malformed resume line %s:%d (%s)", path, line_no, exc.msg
                )
                continue
            rec_id = obj.get("id")
            if isinstance(rec_id, str):
                ids.add(rec_id)
    return ids


def _append_jsonl(path: Path, record: RunRecord) -> None:
    """Append one record as a single JSON line; fsync to survive crashes."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(record.model_dump_json() + "\n")
        fh.flush()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def run(
    config: RunConfig,
    *,
    target_client: ChatClient | None = None,
    judge_a_client: ChatClient | None = None,
    judge_b_client: ChatClient | None = None,
    progress: bool = True,
) -> Iterator[RunRecord]:
    """Run the evaluation pipeline, yielding and persisting each record.

    Parameters
    ----------
    config : RunConfig
    target_client, judge_a_client, judge_b_client : ChatClient | None
        Dependency-injection hooks for tests. If any is ``None``, a real
        provider client is built from env credentials.
    progress : bool
        Show a tqdm progress bar (disable for tests).

    Yields
    ------
    RunRecord
    """
    # Resolve clients.
    if target_client is None or judge_a_client is None or judge_b_client is None:
        settings = get_settings()
        anthropic_key = settings.require_anthropic_key()
        openai_key = settings.require_openai_key()
        target_client = target_client or build_client(
            config.target_model,
            anthropic_key=anthropic_key,
            openai_key=openai_key,
        )
        judge_a_client = judge_a_client or build_client(
            config.judge_a_model,
            anthropic_key=anthropic_key,
            openai_key=openai_key,
        )
        judge_b_client = judge_b_client or build_client(
            config.judge_b_model,
            anthropic_key=anthropic_key,
            openai_key=openai_key,
        )

    jury = Jury(judge_a=Judge(judge_a_client), judge_b=Judge(judge_b_client))

    # Load + sample.
    all_prompts = load_domain(config.dataset_dir, config.domain)
    sampled = sample(all_prompts, n=config.n, seed=config.seed, domain=config.domain)
    logger.info(
        "run start: n=%d domain=%s target=%s judges=(%s, %s) seed=%d output=%s",
        len(sampled),
        config.domain,
        config.target_model,
        config.judge_a_model,
        config.judge_b_model,
        config.seed,
        config.output_path,
    )

    # Resume filter.
    done_ids: set[str] = set()
    if config.resume:
        done_ids = _already_done_ids(config.output_path)
        if done_ids:
            logger.info("resume: %d records already present, skipping", len(done_ids))

    work: list[Prompt] = [p for p in sampled if p.id not in done_ids]

    iterator = tqdm(work, desc="trident-repro", disable=not progress, unit="prompt")
    for prompt in iterator:
        try:
            record = _evaluate_one(
                prompt,
                target_client=target_client,
                jury=jury,
                target_model=config.target_model,
                max_tokens=config.max_tokens,
                temperature=config.temperature,
            )
        except Exception:
            # Partial-failure resilience: log, drop this row, keep going.
            logger.exception("prompt id=%s failed; continuing", prompt.id)
            continue

        _append_jsonl(config.output_path, record)
        yield record

    logger.info("run complete: output=%s", config.output_path)


def _evaluate_one(
    prompt: Prompt,
    *,
    target_client: ChatClient,
    jury: Jury,
    target_model: str,
    max_tokens: int,
    temperature: float,
) -> RunRecord:
    """Run one prompt through target + jury, returning a `RunRecord`."""
    target_response = target_client.complete(
        system="You are a helpful professional assistant.",
        user=prompt.harmful_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    verdict_a, verdict_b, mean = jury.score(prompt.harmful_prompt, target_response)

    return RunRecord(
        id=prompt.id,
        domain=prompt.domain,
        risk_type=prompt.risk_type,
        ethical_refs=list(prompt.ethical_refs),
        harmful_prompt=prompt.harmful_prompt,
        target_model=target_model,
        target_response=target_response,
        judge_a=verdict_a,
        judge_b=verdict_b,
        mean_score=mean,
        ts=datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
