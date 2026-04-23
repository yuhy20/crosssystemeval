"""End-to-end pipeline tests (no real API calls).

The pipeline is exercised with fakes for both target and judges. We verify
that it (a) yields the right number of records, (b) writes each to JSONL
incrementally, (c) resumes correctly from a partial prior run, (d) does not
abort on a single-prompt exception.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests.conftest import FakeChatClient
from trident_repro.config import RunConfig
from trident_repro.pipeline import RunRecord, run


@pytest.fixture
def cfg(tiny_dataset_dir: Path, tmp_path: Path) -> RunConfig:
    return RunConfig(
        n=3,
        domain="law",
        seed=42,
        target_model="fake-target",
        judge_a_model="fake-judge-a",
        judge_b_model="fake-judge-b",
        dataset_dir=tiny_dataset_dir,
        output_path=tmp_path / "outputs" / "run.jsonl",
    )


class TestRunHappyPath:
    def test_yields_records_and_writes_jsonl(
        self,
        cfg: RunConfig,
        fake_clients: tuple[FakeChatClient, FakeChatClient, FakeChatClient],
    ) -> None:
        target, judge_a, judge_b = fake_clients
        records = list(
            run(
                cfg,
                target_client=target,
                judge_a_client=judge_a,
                judge_b_client=judge_b,
                progress=False,
            )
        )

        assert len(records) == 3
        assert all(isinstance(r, RunRecord) for r in records)
        # Each record should carry both judges' scores and the mean.
        for r in records:
            assert r.judge_a.score == 1
            assert r.judge_b.score == 2
            assert r.mean_score == pytest.approx(1.5)

        # JSONL should contain the same three records on disk.
        lines = cfg.output_path.read_text(encoding="utf-8").splitlines()
        assert len(lines) == 3
        on_disk_ids = {json.loads(ln)["id"] for ln in lines}
        assert on_disk_ids == {r.id for r in records}

    def test_calls_target_once_per_prompt(
        self,
        cfg: RunConfig,
        fake_clients: tuple[FakeChatClient, FakeChatClient, FakeChatClient],
    ) -> None:
        target, judge_a, judge_b = fake_clients
        list(
            run(
                cfg,
                target_client=target,
                judge_a_client=judge_a,
                judge_b_client=judge_b,
                progress=False,
            )
        )
        assert len(target.calls) == 3
        assert len(judge_a.calls) == 3
        assert len(judge_b.calls) == 3


class TestResume:
    def test_skips_ids_already_in_output_file(
        self,
        tiny_dataset_dir: Path,
        tmp_path: Path,
        fake_clients: tuple[FakeChatClient, FakeChatClient, FakeChatClient],
    ) -> None:
        out = tmp_path / "outputs" / "run.jsonl"
        out.parent.mkdir(parents=True, exist_ok=True)

        # Figure out which id `sample(n=3, seed=42, domain="law")` would pick
        # first, so we can pre-write it to the output file.
        from trident_repro.loader import load_domain, sample

        prompts = load_domain(tiny_dataset_dir, "law")
        [pre_committed, *_] = sample(prompts, n=3, seed=42, domain="law")

        prewritten = {
            "id": pre_committed.id,
            "domain": pre_committed.domain,
            "risk_type": pre_committed.risk_type,
            "ethical_refs": list(pre_committed.ethical_refs),
            "harmful_prompt": pre_committed.harmful_prompt,
            "target_model": "fake-target",
            "target_response": "pre-existing",
            "judge_a": {"model": "ja", "score": 1, "reasoning": "cached"},
            "judge_b": {"model": "jb", "score": 1, "reasoning": "cached"},
            "mean_score": 1.0,
            "ts": "2026-04-22T00:00:00Z",
        }
        out.write_text(json.dumps(prewritten) + "\n", encoding="utf-8")

        target, judge_a, judge_b = fake_clients
        cfg = RunConfig(
            n=3,
            domain="law",
            seed=42,
            target_model="fake-target",
            judge_a_model="fake-judge-a",
            judge_b_model="fake-judge-b",
            dataset_dir=tiny_dataset_dir,
            output_path=out,
            resume=True,
        )

        new_records = list(
            run(
                cfg,
                target_client=target,
                judge_a_client=judge_a,
                judge_b_client=judge_b,
                progress=False,
            )
        )

        # Expected: 2 new records (3 sampled - 1 already present).
        assert len(new_records) == 2
        assert all(r.id != pre_committed.id for r in new_records)
        # Target was called only for the 2 not-yet-done prompts.
        assert len(target.calls) == 2


class TestPartialFailureResilience:
    def test_continues_after_single_prompt_failure(
        self,
        cfg: RunConfig,
    ) -> None:
        target = FakeChatClient(
            model="fake-target",
            responses=["i refuse", "i refuse", "i refuse"],
            raise_on_calls={1},  # second prompt blows up
        )
        judge_a = FakeChatClient(
            model="fake-judge-a", responses=['{"score": 1}'] * 10
        )
        judge_b = FakeChatClient(
            model="fake-judge-b", responses=['{"score": 2}'] * 10
        )

        records = list(
            run(
                cfg,
                target_client=target,
                judge_a_client=judge_a,
                judge_b_client=judge_b,
                progress=False,
            )
        )

        # 1 failed in the middle; 2 should have survived.
        assert len(records) == 2
        lines = cfg.output_path.read_text(encoding="utf-8").splitlines()
        assert len(lines) == 2


class TestJSONLDurability:
    def test_each_record_appended_immediately(
        self,
        cfg: RunConfig,
        fake_clients: tuple[FakeChatClient, FakeChatClient, FakeChatClient],
    ) -> None:
        """The generator-iterator should flush each record to disk at yield time."""
        target, judge_a, judge_b = fake_clients

        iterator = run(
            cfg,
            target_client=target,
            judge_a_client=judge_a,
            judge_b_client=judge_b,
            progress=False,
        )

        # Consume one record at a time; confirm the file grows in step.
        for i, _ in enumerate(iterator, start=1):
            lines = cfg.output_path.read_text(encoding="utf-8").splitlines()
            assert len(lines) == i
