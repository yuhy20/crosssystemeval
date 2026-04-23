"""Unit tests for `trident_repro.judge`.

Covers the three-tier parser (strict JSON → first balanced `{...}` → regex
fallback), score clamping, `Judge.score` via a fake `ChatClient`, and
`Jury.score` averaging.
"""

from __future__ import annotations

import pytest

from tests.conftest import FakeChatClient
from trident_repro.judge import (
    Judge,
    JudgeVerdict,
    Jury,
    parse_judge_response,
)


# ---------------------------------------------------------------------------
# parse_judge_response
# ---------------------------------------------------------------------------


class TestParseStrict:
    def test_clean_json(self) -> None:
        v = parse_judge_response(
            '{"score": 3, "reasoning": "ambiguous"}', model="judge-x"
        )
        assert v.model == "judge-x"
        assert v.score == 3
        assert v.reasoning == "ambiguous"

    def test_missing_reasoning_defaults_empty(self) -> None:
        v = parse_judge_response('{"score": 1}', model="j")
        assert v.score == 1
        assert v.reasoning == ""


class TestParseBalanced:
    def test_json_wrapped_in_prose(self) -> None:
        raw = 'Sure, here is my verdict:\n{"score": 4, "reasoning": "mostly complies"}\nThanks.'
        v = parse_judge_response(raw, model="j")
        assert v.score == 4
        assert "mostly complies" in v.reasoning

    def test_markdown_codefence(self) -> None:
        raw = '```json\n{"score": 2, "reasoning": "hedged"}\n```'
        v = parse_judge_response(raw, model="j")
        assert v.score == 2


class TestParseRegexFallback:
    def test_malformed_but_score_visible(self) -> None:
        # Trailing comma would trip strict json.loads, which is fine; we
        # just confirm something in this family of malformations still works.
        raw = 'garbage prelude "score": 5, "reasoning": "full compliance" trailing junk'
        v = parse_judge_response(raw, model="j")
        assert v.score == 5
        assert v.reasoning == "full compliance"

    def test_no_score_raises(self) -> None:
        with pytest.raises(ValueError, match="could not parse"):
            parse_judge_response("I cannot comply.", model="j")

    def test_empty_input_raises(self) -> None:
        with pytest.raises(ValueError):
            parse_judge_response("", model="j")


class TestScoreClamping:
    def test_above_5_clamps_to_5(self) -> None:
        v = parse_judge_response('{"score": 9}', model="j")
        assert v.score == 5

    def test_below_1_clamps_to_1(self) -> None:
        v = parse_judge_response('{"score": -2}', model="j")
        assert v.score == 1

    def test_float_coerced_to_int(self) -> None:
        v = parse_judge_response('{"score": 3.7}', model="j")
        assert v.score == 3


class TestJudgeVerdictModel:
    def test_direct_construction_rejects_out_of_range(self) -> None:
        # Validator clamps, so even a direct hit should land in-range.
        v = JudgeVerdict(model="m", score=50)  # type: ignore[arg-type]
        assert v.score == 5

    def test_score_must_be_intlike(self) -> None:
        with pytest.raises(Exception):
            JudgeVerdict(model="m", score="not-a-number")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Judge + Jury behavior (fake ChatClient)
# ---------------------------------------------------------------------------


class TestJudge:
    def test_score_returns_verdict_and_calls_client(self) -> None:
        fake = FakeChatClient(
            model="j1",
            responses=['{"score": 2, "reasoning": "cautious refusal"}'],
        )
        verdict = Judge(fake).score(prompt="P?", response="R.")
        assert verdict.model == "j1"
        assert verdict.score == 2
        assert fake.calls[0]["temperature"] == 0.0
        assert fake.calls[0]["max_tokens"] == 256

    def test_score_propagates_parse_error(self) -> None:
        fake = FakeChatClient(model="j1", responses=["total garbage"])
        with pytest.raises(ValueError):
            Judge(fake).score(prompt="P", response="R")


class TestJury:
    def test_mean_of_two_scores(self) -> None:
        fake_a = FakeChatClient(
            model="ja", responses=['{"score": 2, "reasoning": "r"}']
        )
        fake_b = FakeChatClient(
            model="jb", responses=['{"score": 4, "reasoning": "r"}']
        )
        jury = Jury(judge_a=Judge(fake_a), judge_b=Judge(fake_b))
        va, vb, mean = jury.score(prompt="P", response="R")
        assert va.score == 2
        assert vb.score == 4
        assert mean == 3.0

    def test_exact_agreement_returns_integer_mean(self) -> None:
        fake_a = FakeChatClient(model="ja", responses=['{"score": 1}'])
        fake_b = FakeChatClient(model="jb", responses=['{"score": 1}'])
        jury = Jury(judge_a=Judge(fake_a), judge_b=Judge(fake_b))
        _, _, mean = jury.score(prompt="P", response="R")
        assert mean == 1.0
