"""trident_repro: LLM-as-judge calibration harness for a subset of TRIDENT.

Public re-exports are intentionally small. Callers should import sub-modules
for anything specialized.
"""

from __future__ import annotations

from trident_repro.config import RunConfig, Settings, get_settings
from trident_repro.judge import JUDGE_SYSTEM_PROMPT, Judge, JudgeVerdict, Jury
from trident_repro.loader import Prompt, load_jsonl, sample
from trident_repro.pipeline import RunRecord, run

__version__ = "0.1.0"

__all__ = [
    "JUDGE_SYSTEM_PROMPT",
    "Judge",
    "JudgeVerdict",
    "Jury",
    "Prompt",
    "RunConfig",
    "RunRecord",
    "Settings",
    "__version__",
    "get_settings",
    "load_jsonl",
    "run",
    "sample",
]
