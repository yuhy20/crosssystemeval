"""Command-line entry point for trident-repro.

Exposed as the `trident-repro` console script (see pyproject.toml).
"""

from __future__ import annotations

import logging
import sys
from datetime import UTC, datetime
from pathlib import Path

import click

from trident_repro import __version__
from trident_repro.config import (
    DEFAULT_DATASET_DIR,
    DEFAULT_JUDGE_A,
    DEFAULT_JUDGE_B,
    DEFAULT_TARGET_MODEL,
    RunConfig,
    configure_logging,
    get_settings,
)
from trident_repro.metrics import aggregate, format_report, load_records

logger = logging.getLogger("trident_repro.cli")


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(__version__, prog_name="trident-repro")
def cli() -> None:
    """TRIDENT LLM-as-judge calibration harness."""


# ---------------------------------------------------------------------------
# run
# ---------------------------------------------------------------------------


@cli.command("run")
@click.option("--n", type=int, required=True, help="Number of prompts to sample.")
@click.option(
    "--domain",
    type=click.Choice(["law", "med", "finance", "all"]),
    required=True,
    help="TRIDENT domain to sample from.",
)
@click.option(
    "--target-model",
    default=DEFAULT_TARGET_MODEL,
    show_default=True,
    help="Model under evaluation.",
)
@click.option(
    "--judge-a",
    "judge_a_model",
    default=DEFAULT_JUDGE_A,
    show_default=True,
    help="Judge A model id (Anthropic by default).",
)
@click.option(
    "--judge-b",
    "judge_b_model",
    default=DEFAULT_JUDGE_B,
    show_default=True,
    help="Judge B model id (OpenAI by default).",
)
@click.option("--seed", type=int, default=42, show_default=True, help="Sampling seed.")
@click.option(
    "--dataset-dir",
    type=click.Path(path_type=Path, file_okay=False, dir_okay=True),
    default=DEFAULT_DATASET_DIR,
    show_default=True,
    help="Directory containing *_final.jsonl dataset files.",
)
@click.option(
    "--output",
    "output_path",
    type=click.Path(path_type=Path, file_okay=True, dir_okay=False),
    default=None,
    help="JSONL output file. Default: outputs/run_<UTC-timestamp>.jsonl.",
)
@click.option(
    "--resume",
    is_flag=True,
    default=False,
    help="Skip prompts whose id already appears in the output file.",
)
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"]),
    default=None,
    help="Override TRIDENT_LOG_LEVEL.",
)
@click.option(
    "--no-progress",
    is_flag=True,
    default=False,
    help="Disable tqdm progress bar.",
)
def run_cmd(
    n: int,
    domain: str,
    target_model: str,
    judge_a_model: str,
    judge_b_model: str,
    seed: int,
    dataset_dir: Path,
    output_path: Path | None,
    resume: bool,
    log_level: str | None,
    no_progress: bool,
) -> None:
    """Sample N prompts, evaluate with target model, score via 2-model jury."""
    settings = get_settings()
    configure_logging(log_level or settings.TRIDENT_LOG_LEVEL)

    if output_path is None:
        stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        output_path = Path("outputs") / f"run_{stamp}.jsonl"

    config = RunConfig(
        n=n,
        domain=domain,  # type: ignore[arg-type]
        seed=seed,
        target_model=target_model,
        judge_a_model=judge_a_model,
        judge_b_model=judge_b_model,
        dataset_dir=dataset_dir,
        output_path=output_path,
        resume=resume,
    )

    # Fail fast on missing credentials before doing any real work.
    settings.require_anthropic_key()
    settings.require_openai_key()

    # Lazy import: avoids pulling heavy provider SDKs during `--help`.
    from trident_repro.pipeline import run as pipeline_run

    count = 0
    for _ in pipeline_run(config, progress=not no_progress):
        count += 1

    click.echo(f"wrote {count} records -> {output_path}")


# ---------------------------------------------------------------------------
# aggregate
# ---------------------------------------------------------------------------


@cli.command("aggregate")
@click.option(
    "--input",
    "input_path",
    type=click.Path(path_type=Path, exists=True, dir_okay=False),
    required=True,
    help="Run JSONL to summarize.",
)
@click.option(
    "--json",
    "as_json",
    is_flag=True,
    default=False,
    help="Emit machine-readable JSON instead of the text report.",
)
def aggregate_cmd(input_path: Path, as_json: bool) -> None:
    """Print per-domain means, inter-judge agreement, published-delta."""
    configure_logging("WARNING")  # keep output clean by default
    records = load_records(input_path)
    agg = aggregate(records)
    if as_json:
        from trident_repro.metrics import aggregate_to_json

        click.echo(aggregate_to_json(agg))
    else:
        click.echo(format_report(agg))


def main() -> int:
    """Script entry point used for manual invocation."""
    try:
        cli()
    except Exception:
        logger.exception("fatal error")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
