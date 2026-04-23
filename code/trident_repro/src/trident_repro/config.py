"""Configuration: environment-driven `Settings` and a per-run `RunConfig`.

`Settings` loads secrets (API keys) from `.env` via pydantic-settings.
`RunConfig` is the immutable, fully-resolved description of a single
evaluation run, constructed from CLI flags + defaults.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

Domain = Literal["law", "med", "finance", "all"]

DEFAULT_DATASET_DIR = Path(
    Path(__file__).resolve().parents[4] / "data" / "TRIDENT" / "dataset"
)
DEFAULT_JUDGE_A = "claude-3-5-sonnet-20241022"
DEFAULT_JUDGE_B = "gpt-4o-mini"
DEFAULT_TARGET_MODEL = "claude-3-5-sonnet-20241022"


class Settings(BaseSettings):
    """Environment-backed configuration.

    Values are loaded from `.env` (if present) and the process environment.
    Missing keys raise clear errors at access time rather than silently
    passing `None` to an SDK client.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    ANTHROPIC_API_KEY: SecretStr | None = Field(
        default=None, description="Anthropic API key."
    )
    OPENAI_API_KEY: SecretStr | None = Field(
        default=None, description="OpenAI API key."
    )
    TRIDENT_DATASET_DIR: Path = Field(
        default=DEFAULT_DATASET_DIR,
        description="Directory containing `*_final.jsonl` dataset files.",
    )
    TRIDENT_LOG_LEVEL: str = Field(
        default="INFO", description="Python logging level name."
    )

    def require_anthropic_key(self) -> str:
        """Return the Anthropic API key or raise a clear error."""
        if self.ANTHROPIC_API_KEY is None:
            raise RuntimeError(
                "ANTHROPIC_API_KEY is not set. Copy .env.example to .env and fill it in."
            )
        return self.ANTHROPIC_API_KEY.get_secret_value()

    def require_openai_key(self) -> str:
        """Return the OpenAI API key or raise a clear error."""
        if self.OPENAI_API_KEY is None:
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Copy .env.example to .env and fill it in."
            )
        return self.OPENAI_API_KEY.get_secret_value()


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Cached accessor. Re-reads `.env` only once per process."""
    return Settings()


@dataclass(frozen=True, slots=True)
class RunConfig:
    """Immutable description of one calibration run."""

    n: int
    domain: Domain
    seed: int
    target_model: str = DEFAULT_TARGET_MODEL
    judge_a_model: str = DEFAULT_JUDGE_A
    judge_b_model: str = DEFAULT_JUDGE_B
    dataset_dir: Path = DEFAULT_DATASET_DIR
    output_path: Path = Path("outputs/run.jsonl")
    resume: bool = False
    max_tokens: int = 1024
    temperature: float = 0.0

    def __post_init__(self) -> None:
        if self.n <= 0:
            raise ValueError(f"n must be positive, got {self.n}")
        if self.domain not in ("law", "med", "finance", "all"):
            raise ValueError(f"invalid domain {self.domain!r}")
        if not (0.0 <= self.temperature <= 2.0):
            raise ValueError(f"temperature must be in [0, 2], got {self.temperature}")


def configure_logging(level: str | int = "INFO") -> None:
    """Idempotent root-logger configuration.

    Uses a structured-ish single-line format: timestamp, level, logger, message.
    Safe to call from the CLI or tests; subsequent calls reset handlers.
    """
    root = logging.getLogger()
    for handler in list(root.handlers):
        root.removeHandler(handler)

    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s %(levelname)-7s %(name)s | %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
    )
    root.addHandler(handler)
    root.setLevel(level if isinstance(level, int) else level.upper())
