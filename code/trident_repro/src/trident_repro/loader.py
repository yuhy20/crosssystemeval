"""Dataset loading and deterministic sampling.

TRIDENT records look like::

    {
      "domain": "law",
      "ethical_refs": ["Rule 4.1 - Truthfulness in Statements"],
      "harmful_prompt": "...",
      "id": "uuid",
      "risk_type": "third_party_dishonesty",
      "safe_reply": "..."
    }
"""

from __future__ import annotations

import json
import logging
import random
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

logger = logging.getLogger(__name__)

Domain = Literal["law", "med", "finance", "all"]

# Map public domain name -> dataset filename stem.
_DOMAIN_FILES: dict[str, str] = {
    "law": "law_final.jsonl",
    "med": "med_final.jsonl",
    "finance": "finance_final.jsonl",
}


class Prompt(BaseModel):
    """One TRIDENT prompt row."""

    model_config = ConfigDict(extra="ignore", frozen=True)

    id: str
    domain: str
    risk_type: str = Field(default="unknown")
    ethical_refs: list[str] = Field(default_factory=list)
    harmful_prompt: str
    safe_reply: str | None = None


def load_jsonl(path: Path) -> list[Prompt]:
    """Load a single TRIDENT-format JSONL file into validated `Prompt`s.

    Raises
    ------
    FileNotFoundError
        If `path` does not exist.
    pydantic.ValidationError
        If a record fails schema validation.
    """
    if not path.exists():
        raise FileNotFoundError(f"Dataset file not found: {path}")

    prompts: list[Prompt] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_no, raw in enumerate(fh, start=1):
            line = raw.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"{path}:{line_no}: invalid JSON ({exc.msg})"
                ) from exc
            prompts.append(Prompt.model_validate(obj))
    logger.info("loaded %d prompts from %s", len(prompts), path)
    return prompts


def load_domain(dataset_dir: Path, domain: Domain) -> list[Prompt]:
    """Load every record for `domain`. `domain='all'` concatenates all three."""
    if domain == "all":
        out: list[Prompt] = []
        for name in ("law", "med", "finance"):
            out.extend(load_jsonl(dataset_dir / _DOMAIN_FILES[name]))
        return out

    if domain not in _DOMAIN_FILES:
        raise ValueError(f"unknown domain {domain!r}")
    return load_jsonl(dataset_dir / _DOMAIN_FILES[domain])


def sample(
    prompts: list[Prompt],
    n: int,
    seed: int,
    domain: Domain | None = None,
) -> list[Prompt]:
    """Deterministic k-sample without replacement.

    Parameters
    ----------
    prompts : list[Prompt]
    n : int
        Number of samples to draw. If `n >= len(eligible)`, returns all
        eligible prompts (still shuffled by `seed`).
    seed : int
        Seed for `random.Random`. Same seed + same input -> identical output.
    domain : Domain | None
        If set and not ``"all"``, filters `prompts` to that domain first.
    """
    if n <= 0:
        raise ValueError(f"n must be positive, got {n}")

    eligible: list[Prompt]
    if domain is None or domain == "all":
        eligible = list(prompts)
    else:
        eligible = [p for p in prompts if p.domain == domain]

    rng = random.Random(seed)
    shuffled = eligible[:]
    rng.shuffle(shuffled)
    return shuffled[: min(n, len(shuffled))]
