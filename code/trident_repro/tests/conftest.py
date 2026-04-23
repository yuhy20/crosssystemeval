"""Shared pytest fixtures.

Deliberately kept small: the test suite is mock-based and does not hit any
real LLM provider. Fakes live here so each test module doesn't re-implement
the `ChatClient` protocol.
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Fake ChatClient
# ---------------------------------------------------------------------------


@dataclass
class FakeChatClient:
    """Scriptable fake satisfying the `ChatClient` protocol.

    Either pass `responses=[...]` (consumed in order) for deterministic
    replay, or `responder=lambda system, user, **kw: "..."` for more
    flexible behavior (e.g., raising on a specific user prompt).
    """

    model: str = "fake-model"
    responses: list[str] = field(default_factory=list)
    responder: object = None  # callable or None
    calls: list[dict[str, object]] = field(default_factory=list)
    raise_on_calls: set[int] = field(default_factory=set)

    def complete(
        self,
        *,
        system: str,
        user: str,
        max_tokens: int = 1024,
        temperature: float = 0.0,
    ) -> str:
        call_index = len(self.calls)
        self.calls.append(
            {
                "system": system,
                "user": user,
                "max_tokens": max_tokens,
                "temperature": temperature,
            }
        )
        if call_index in self.raise_on_calls:
            raise RuntimeError(f"fake client configured to raise on call {call_index}")
        if self.responder is not None:
            return self.responder(system=system, user=user)  # type: ignore[operator]
        if not self.responses:
            raise AssertionError(
                "FakeChatClient exhausted: no responses left and no responder set"
            )
        return self.responses.pop(0)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _sample_prompt_row(
    id_: str, domain: str, harmful_prompt: str = "dummy prompt"
) -> dict[str, object]:
    return {
        "id": id_,
        "domain": domain,
        "risk_type": f"{domain}_risk",
        "ethical_refs": [f"Rule {id_}"],
        "harmful_prompt": harmful_prompt,
        "safe_reply": "refuse politely",
    }


@pytest.fixture
def tiny_dataset_dir(tmp_path: Path) -> Path:
    """Write a minimal TRIDENT-shaped dataset to a temp dir and return its path."""
    rows_law = [_sample_prompt_row(f"law-{i}", "law") for i in range(5)]
    rows_med = [_sample_prompt_row(f"med-{i}", "med") for i in range(3)]
    rows_fin = [_sample_prompt_row(f"fin-{i}", "finance") for i in range(2)]

    for name, rows in (
        ("law_final.jsonl", rows_law),
        ("med_final.jsonl", rows_med),
        ("finance_final.jsonl", rows_fin),
    ):
        path = tmp_path / name
        with path.open("w", encoding="utf-8") as fh:
            for row in rows:
                fh.write(json.dumps(row) + "\n")

    return tmp_path


@pytest.fixture
def fake_clients() -> Iterator[tuple[FakeChatClient, FakeChatClient, FakeChatClient]]:
    """Three fakes: target, judge-a, judge-b. Pre-populated with sane defaults."""
    target = FakeChatClient(model="fake-target", responses=["i refuse to do that"] * 20)
    judge_a = FakeChatClient(
        model="fake-judge-a",
        responses=['{"score": 1, "reasoning": "clear refusal"}'] * 20,
    )
    judge_b = FakeChatClient(
        model="fake-judge-b",
        responses=['{"score": 2, "reasoning": "compliant but cautious"}'] * 20,
    )
    yield target, judge_a, judge_b
