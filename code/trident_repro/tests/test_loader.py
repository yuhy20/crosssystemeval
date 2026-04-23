"""Unit tests for `trident_repro.loader`.

Covers: schema validation, malformed-line handling, blank-line tolerance,
`extra="ignore"` semantics, and deterministic sampling under fixed seed.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from trident_repro.loader import (
    Prompt,
    load_domain,
    load_jsonl,
    sample,
)


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row) + "\n")


class TestLoadJsonl:
    def test_loads_valid_records(self, tmp_path: Path) -> None:
        path = tmp_path / "t.jsonl"
        _write_jsonl(
            path,
            [
                {
                    "id": "a",
                    "domain": "law",
                    "risk_type": "x",
                    "ethical_refs": ["Rule 1"],
                    "harmful_prompt": "p1",
                    "safe_reply": "r1",
                },
                {
                    "id": "b",
                    "domain": "law",
                    "risk_type": "y",
                    "ethical_refs": [],
                    "harmful_prompt": "p2",
                },
            ],
        )
        prompts = load_jsonl(path)
        assert len(prompts) == 2
        assert prompts[0].id == "a"
        assert prompts[0].ethical_refs == ["Rule 1"]
        assert prompts[1].safe_reply is None

    def test_missing_file_raises(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            load_jsonl(tmp_path / "nope.jsonl")

    def test_malformed_json_raises_valueerror(self, tmp_path: Path) -> None:
        path = tmp_path / "bad.jsonl"
        path.write_text('{"id": "a", "domain": "law", "harmful_prompt": "ok"}\n{not json\n')
        with pytest.raises(ValueError, match="invalid JSON"):
            load_jsonl(path)

    def test_blank_lines_are_skipped(self, tmp_path: Path) -> None:
        path = tmp_path / "blanks.jsonl"
        path.write_text(
            '{"id": "a", "domain": "law", "harmful_prompt": "p"}\n'
            "\n"
            "   \n"
            '{"id": "b", "domain": "law", "harmful_prompt": "q"}\n',
        )
        prompts = load_jsonl(path)
        assert [p.id for p in prompts] == ["a", "b"]

    def test_extra_fields_ignored(self, tmp_path: Path) -> None:
        path = tmp_path / "extra.jsonl"
        _write_jsonl(
            path,
            [
                {
                    "id": "a",
                    "domain": "law",
                    "harmful_prompt": "p",
                    "unexpected_field": "whatever",
                }
            ],
        )
        [prompt] = load_jsonl(path)
        assert prompt.id == "a"

    def test_missing_required_field_raises(self, tmp_path: Path) -> None:
        path = tmp_path / "missing.jsonl"
        _write_jsonl(path, [{"id": "a", "domain": "law"}])  # no harmful_prompt
        with pytest.raises(ValidationError):
            load_jsonl(path)


class TestLoadDomain:
    def test_single_domain(self, tiny_dataset_dir: Path) -> None:
        prompts = load_domain(tiny_dataset_dir, "law")
        assert len(prompts) == 5
        assert all(p.domain == "law" for p in prompts)

    def test_all_domains_concatenated(self, tiny_dataset_dir: Path) -> None:
        prompts = load_domain(tiny_dataset_dir, "all")
        # fixture seeds 5 law + 3 med + 2 finance
        assert len(prompts) == 10
        assert {p.domain for p in prompts} == {"law", "med", "finance"}

    def test_unknown_domain_raises(self, tiny_dataset_dir: Path) -> None:
        with pytest.raises(ValueError, match="unknown domain"):
            load_domain(tiny_dataset_dir, "bogus")  # type: ignore[arg-type]


class TestSample:
    @pytest.fixture
    def pool(self) -> list[Prompt]:
        return [
            Prompt(id=f"p{i}", domain="law" if i % 2 == 0 else "med", harmful_prompt=f"q{i}")
            for i in range(20)
        ]

    def test_deterministic_same_seed(self, pool: list[Prompt]) -> None:
        a = sample(pool, n=5, seed=42)
        b = sample(pool, n=5, seed=42)
        assert [p.id for p in a] == [p.id for p in b]

    def test_different_seeds_differ(self, pool: list[Prompt]) -> None:
        a = sample(pool, n=5, seed=1)
        b = sample(pool, n=5, seed=2)
        # Not a guarantee in the worst case, but with n=5 from a 20-pool
        # collision on all 5 elements is vanishingly unlikely.
        assert [p.id for p in a] != [p.id for p in b]

    def test_without_replacement(self, pool: list[Prompt]) -> None:
        result = sample(pool, n=10, seed=0)
        ids = [p.id for p in result]
        assert len(ids) == len(set(ids))

    def test_n_greater_than_eligible_returns_all(self, pool: list[Prompt]) -> None:
        result = sample(pool, n=1000, seed=0)
        assert len(result) == len(pool)

    def test_domain_filter(self, pool: list[Prompt]) -> None:
        result = sample(pool, n=100, seed=0, domain="law")
        assert all(p.domain == "law" for p in result)
        assert len(result) == 10  # half the pool

    def test_non_positive_n_raises(self, pool: list[Prompt]) -> None:
        with pytest.raises(ValueError, match="must be positive"):
            sample(pool, n=0, seed=0)
        with pytest.raises(ValueError, match="must be positive"):
            sample(pool, n=-3, seed=0)
