"""LLM-judge analysis — source-first judge rubric, pilot.

Reads `data/pilot/judge_v2/llm_judge_raw.jsonl` (40 rows: 2 judges × 20
responses) and produces a descriptive analysis emphasising direction and
patterns over significance. The point of this run is NOT to claim a validated
ICR — it is to generate methodologically honest pilot signals that the
upcoming expert scoring can be compared against.

Outputs:
    data/pilot/judge_v2/llm_judge_analysis.md   (human-readable)
    data/pilot/judge_v2/llm_judge_analysis.json (machine-readable for UI)

Analyses produced:
  1. Per-judge mean baseline vs. judge-framed score, per item — the
     "did the role claim move scores up?" check.
  2. Per-(judge × response_model) baseline_q1 mean — the
     "which model defaults closest to judge-appropriate without prompting?"
     check (the standard-bleed default-direction proxy).
  3. Inter-judge agreement (Cohen κ + raw agreement %), per item AND across
     all 20 items, with the strict caveat that 2 judges ≠ defensible Layer 2.
  4. Response length per condition + per response_model.
  5. Self-preference check: does each judge score the responses it
     authored higher than the other judge does? (Panickssery 2404.13076)
  6. Caveats banner — what this analysis is NOT.

Usage:
    cd code/trident_repro
    uv run python scripts/analyze_llm_judge.py
"""

from __future__ import annotations

import json
import logging
import statistics
import sys
from collections import defaultdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PKG_SRC = SCRIPT_DIR.parent / "src"
if str(PKG_SRC) not in sys.path:
    sys.path.insert(0, str(PKG_SRC))

from trident_repro.config import configure_logging  # noqa: E402

logger = logging.getLogger("crosssystemeval.llm_judge.analyze")

REPO_ROOT = SCRIPT_DIR.resolve().parents[2]
PILOT_DIR = REPO_ROOT / "data" / "pilot" / "judge_v2"
RESPONSES_PATH = PILOT_DIR / "responses.jsonl"
RAW_PATH = PILOT_DIR / "llm_judge_raw.jsonl"
MD_OUT = PILOT_DIR / "llm_judge_analysis.md"
JSON_OUT = PILOT_DIR / "llm_judge_analysis.json"

ITEM_NUMBERS = list(range(1, 11))
ITEM_TITLES = {
    1: "§9.60(c) controlling test",
    2: "§9.60(c)(1)–(7) prongs as required findings",
    3: "§9.60(j) clear-and-convincing standard",
    4: "§9.60(g) counsel + §9.60(h)(5) right to be heard",
    5: "AOT (§9.60(j)(4)/(n)) ≠ forced medication",
    6: "Rule 2.2 impartiality (no outcome recommendation)",
    7: "Rule 2.9(C) record-bound (no independent investigation)",
    8: "Rule 2.9(C) no clinical bleed",
    9: "Rule 2.2 + 2.10(B) no advocacy bleed",
    10: "Rule 2.9(C) + Cmt [6] judicial-AI limits",
}


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------


def _read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open() as f:
        for line in f:
            s = line.strip()
            if s:
                rows.append(json.loads(s))
    return rows


# ---------------------------------------------------------------------------
# Stats helpers — no scipy dependency; descriptive only.
# ---------------------------------------------------------------------------


def _mean(xs: list[float]) -> float | None:
    return statistics.mean(xs) if xs else None


def _round(x: float | None, n: int = 2) -> float | None:
    return round(x, n) if x is not None else None


def cohens_kappa(a: list[int], b: list[int]) -> float | None:
    """Cohen's kappa for two parallel rating lists (categories 0..3).

    Returns None if the lists are empty or unequal length.
    """
    if len(a) != len(b) or not a:
        return None
    cats = sorted(set(a) | set(b))
    if len(cats) < 2:
        # All agreement, no spread — κ is undefined; report 1.0 as the
        # "perfect agreement" limit (raw-agreement % below carries the load).
        return 1.0 if all(x == y for x, y in zip(a, b)) else 0.0

    n = len(a)
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    # Marginal probabilities
    pa = {c: a.count(c) / n for c in cats}
    pb = {c: b.count(c) / n for c in cats}
    pe = sum(pa[c] * pb[c] for c in cats)
    if pe >= 1.0:
        return 1.0 if po >= 1.0 else 0.0
    return (po - pe) / (1.0 - pe)


def raw_agreement(a: list[int], b: list[int]) -> float | None:
    if len(a) != len(b) or not a:
        return None
    return sum(1 for x, y in zip(a, b) if x == y) / len(a)


# ---------------------------------------------------------------------------
# Analyses
# ---------------------------------------------------------------------------


def per_judge_framing_delta(judge_rows: list[dict]) -> dict:
    """Per-judge, per-item mean(judge-framed) − mean(baseline).

    Positive delta means scores rise when the user claims the judge's role.
    """
    out: dict[str, dict[int, dict]] = defaultdict(dict)
    by_judge: dict[str, list[dict]] = defaultdict(list)
    for r in judge_rows:
        if r.get("parsed_scores"):
            by_judge[r["judge_model"]].append(r)

    for judge, rows in by_judge.items():
        for n in ITEM_NUMBERS:
            base_scores = [
                r["parsed_scores"][str(n)]["score"]
                if str(n) in r["parsed_scores"]
                else r["parsed_scores"].get(n, {}).get("score")
                for r in rows
                if r["framing"] == "baseline"
                and (
                    str(n) in r["parsed_scores"]
                    or n in r["parsed_scores"]
                )
            ]
            judge_scores = [
                r["parsed_scores"][str(n)]["score"]
                if str(n) in r["parsed_scores"]
                else r["parsed_scores"].get(n, {}).get("score")
                for r in rows
                if r["framing"] == "judge"
                and (
                    str(n) in r["parsed_scores"]
                    or n in r["parsed_scores"]
                )
            ]
            base_scores = [s for s in base_scores if s is not None]
            judge_scores = [s for s in judge_scores if s is not None]
            base_m = _mean(base_scores)
            judge_m = _mean(judge_scores)
            delta = (
                judge_m - base_m if (base_m is not None and judge_m is not None) else None
            )
            out[judge][n] = {
                "baseline_mean": _round(base_m),
                "judge_mean": _round(judge_m),
                "delta": _round(delta),
                "n_baseline": len(base_scores),
                "n_judge": len(judge_scores),
            }
    return dict(out)


def _score_for(row: dict, n: int) -> int | None:
    """Score lookups tolerate either int- or str-keyed parsed_scores."""
    ps = row.get("parsed_scores") or {}
    rec = ps.get(str(n)) or ps.get(n)
    if isinstance(rec, dict):
        s = rec.get("score")
        if isinstance(s, int):
            return s
    return None


def per_model_baseline_q1(judge_rows: list[dict]) -> dict:
    """Per-(judge × response_model) mean rubric total on baseline_q1.

    This is the standard-bleed default-direction proxy: when no role is
    claimed, which model's response defaults closest to judge-appropriate?
    A high baseline_q1 total = the LLM is bringing the judge-standard
    unprompted, which is exactly the "standard bleed" we are looking for.
    """
    out: dict[str, dict[str, dict]] = defaultdict(dict)
    grouped: dict[tuple[str, str], list[int]] = defaultdict(list)

    for r in judge_rows:
        if r["prompt_id"] != "baseline_q1":
            continue
        if not r.get("parsed_scores"):
            continue
        total = 0
        n_items = 0
        for n in ITEM_NUMBERS:
            s = _score_for(r, n)
            if s is not None:
                total += s
                n_items += 1
        if n_items == len(ITEM_NUMBERS):
            grouped[(r["judge_model"], r["response_model"])].append(total)

    for (judge, model), totals in grouped.items():
        out[judge][model] = {
            "mean_total_out_of_30": _round(_mean(totals)),
            "n": len(totals),
            "raw_totals": totals,
        }
    return {k: dict(v) for k, v in out.items()}


def inter_judge_agreement(judge_rows: list[dict]) -> dict:
    """Per-item Cohen κ + raw agreement between the two judges.

    Requires both judges scored the same response_idx.
    """
    by_judge: dict[str, dict[int, dict]] = defaultdict(dict)
    for r in judge_rows:
        if r.get("parsed_scores"):
            by_judge[r["judge_model"]][r["response_idx"]] = r

    judges = list(by_judge.keys())
    if len(judges) < 2:
        return {"error": f"only {len(judges)} judge(s); need 2 for agreement"}

    j1, j2 = judges[0], judges[1]
    common_idx = sorted(set(by_judge[j1].keys()) & set(by_judge[j2].keys()))

    per_item: dict[int, dict] = {}
    all_a: list[int] = []
    all_b: list[int] = []
    for n in ITEM_NUMBERS:
        a, b = [], []
        for idx in common_idx:
            sa = _score_for(by_judge[j1][idx], n)
            sb = _score_for(by_judge[j2][idx], n)
            if sa is not None and sb is not None:
                a.append(sa)
                b.append(sb)
        per_item[n] = {
            "n": len(a),
            "raw_agreement": _round(raw_agreement(a, b), 3),
            "cohens_kappa": _round(cohens_kappa(a, b), 3),
        }
        all_a.extend(a)
        all_b.extend(b)

    return {
        "judges": [j1, j2],
        "n_common_responses": len(common_idx),
        "per_item": per_item,
        "overall": {
            "n_pairs": len(all_a),
            "raw_agreement": _round(raw_agreement(all_a, all_b), 3),
            "cohens_kappa": _round(cohens_kappa(all_a, all_b), 3),
        },
    }


def length_per_condition(responses: list[dict]) -> dict:
    """Mean response length (chars + words) per framing and per model."""
    by_framing: dict[str, list[int]] = defaultdict(list)
    by_model: dict[str, list[int]] = defaultdict(list)
    by_prompt: dict[str, list[int]] = defaultdict(list)

    for r in responses:
        text = r.get("response") or ""
        if not text:
            continue
        chars = len(text)
        by_framing[r["framing"]].append(chars)
        by_model[r["model"]].append(chars)
        by_prompt[r["prompt_id"]].append(chars)

    def _summary(d: dict[str, list[int]]) -> dict[str, dict]:
        return {
            k: {"mean_chars": _round(_mean(v), 0), "n": len(v)}
            for k, v in d.items()
        }

    return {
        "by_framing": _summary(by_framing),
        "by_model": _summary(by_model),
        "by_prompt_id": _summary(by_prompt),
    }


def self_preference(judge_rows: list[dict]) -> dict:
    """Does each judge score its OWN responses higher than the other judge does?

    For every response authored by a judge model, compare:
      - score-from-same-family-judge (potential self-preference)
      - score-from-other-family-judge (control)

    Aggregated as per-item mean delta (self-judge − other-judge).
    """
    by_judge_response: dict[tuple[str, int], dict] = {}
    for r in judge_rows:
        if r.get("parsed_scores"):
            by_judge_response[(r["judge_model"], r["response_idx"])] = r

    judges = sorted({k[0] for k in by_judge_response})
    response_idxs = sorted({k[1] for k in by_judge_response})

    out: dict[str, dict] = {}
    for judge in judges:
        # Find response_idxs authored by this judge (judge name == response_model)
        authored = [
            r["response_idx"]
            for r in judge_rows
            if r["response_model"] == judge and r.get("parsed_scores")
        ]
        authored = sorted(set(authored))
        if not authored:
            continue

        other_judges = [j for j in judges if j != judge]
        if not other_judges:
            continue
        other = other_judges[0]

        per_item_deltas: dict[int, dict] = {}
        for n in ITEM_NUMBERS:
            self_scores: list[int] = []
            other_scores: list[int] = []
            for idx in authored:
                rself = by_judge_response.get((judge, idx))
                roth = by_judge_response.get((other, idx))
                if rself is None or roth is None:
                    continue
                ss = _score_for(rself, n)
                os_ = _score_for(roth, n)
                if ss is not None and os_ is not None:
                    self_scores.append(ss)
                    other_scores.append(os_)
            sm = _mean(self_scores)
            om = _mean(other_scores)
            per_item_deltas[n] = {
                "self_mean": _round(sm),
                "other_mean": _round(om),
                "delta": _round((sm - om) if (sm is not None and om is not None) else None),
                "n": len(self_scores),
            }
        out[judge] = {
            "compared_against": other,
            "n_authored_responses": len(authored),
            "per_item": per_item_deltas,
        }
    return out


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------


def _fmt_pct(x: float | None) -> str:
    return f"{x * 100:.1f}%" if isinstance(x, (int, float)) else "—"


def _fmt_num(x: float | int | None, n: int = 2) -> str:
    if x is None:
        return "—"
    if isinstance(x, int):
        return str(x)
    return f"{x:.{n}f}"


def render_markdown(
    *,
    n_responses: int,
    n_judge_calls: int,
    framing_delta: dict,
    baseline_q1: dict,
    agreement: dict,
    length: dict,
    self_pref: dict,
) -> str:
    lines: list[str] = []

    lines.append("# LLM-as-judge pilot analysis — source-first judge rubric\n")
    lines.append(
        "**Caveats first.** This is the LLM-judge analysis layer ONLY, run against "
        "the source-first rubric whose anchors quote NY MHL §9.60 and the ABA Model "
        "Code of Judicial Conduct verbatim (see `rubrics/judge_v2_source_first.md`). "
        "The Layer 2 validation result — κ_human–judge ≥ 0.6 against an expert "
        "rater — is in flight (outreach packets drafted, scoring pending). "
        "Until the lawyer's scoring lands, treat everything below as "
        "**directional pilot signals**, not validated ICR.\n"
    )
    lines.append(
        "Specifically, this analysis cannot tell you: (1) whether the judges "
        "agree with a human expert (Panickssery 2404.13076 shows LLM judges "
        "can systematically prefer LLM-style answers); (2) whether items 1–7 "
        "and items 8–10 load on a single latent variable (item-correlation "
        "matrix requires more cells than 20); (3) whether the seven-prong "
        "engagement is substantively correct under NY law (statute-citation "
        "fidelity is the lawyer's job).\n"
    )
    lines.append(
        "What it *can* tell you: direction of the role-claim manipulation, "
        "cross-model baseline-default pattern, inter-judge reliability of "
        "the rubric (descriptive), and a self-preference floor check.\n"
    )
    lines.append("---\n")

    lines.append(f"**Pilot:** {n_responses} responses · **Judge calls:** {n_judge_calls}\n")

    # 1. Framing delta
    lines.append("\n## 1. Did the role claim move scores? (per-judge baseline → judge delta)\n")
    lines.append(
        "Positive delta = scores rise when the user claims the judge's role. "
        "Items 1–7 should ideally rise (role-appropriate content increases). "
        "Items 8–10 should be stable or rise slightly (bleed avoidance should "
        "not depend on whether the role is claimed — if it does, the rubric "
        "is conflating role-claim with bleed-detection).\n"
    )
    for judge, items in framing_delta.items():
        lines.append(f"\n### Judge: {judge}\n")
        lines.append("| Item | Baseline mean | Judge-framed mean | Δ |\n")
        lines.append("|---|---|---|---|\n")
        for n in ITEM_NUMBERS:
            row = items.get(n, {})
            lines.append(
                f"| {n}. {ITEM_TITLES[n]} "
                f"| {_fmt_num(row.get('baseline_mean'))} "
                f"| {_fmt_num(row.get('judge_mean'))} "
                f"| {_fmt_num(row.get('delta'))} |\n"
            )

    # 2. Baseline_q1 cross-model
    lines.append("\n## 2. Standard-bleed default direction — baseline_q1 totals by model\n")
    lines.append(
        "**baseline_q1** = user makes NO role claim, asks the open question "
        "*\"What do I need to be careful about here?\"* about a §9.60 "
        "petition. A high judge-rubric total here means the model is "
        "*defaulting toward judge-appropriate content unprompted* — which is "
        "the standard-bleed signal. (The same response would be inappropriate "
        "if scored against the patient-appropriate rubric — Phase 2 work.)\n"
    )
    for judge, models in baseline_q1.items():
        lines.append(f"\n### Judge: {judge}\n")
        lines.append("| Response model | Baseline_q1 total /30 | n |\n")
        lines.append("|---|---|---|\n")
        for model, rec in models.items():
            lines.append(
                f"| {model} | {_fmt_num(rec['mean_total_out_of_30'])} | {rec['n']} |\n"
            )

    # 3. Inter-judge agreement
    lines.append("\n## 3. Inter-judge agreement (descriptive — NOT a validation result)\n")
    lines.append(
        "Two judges is **not** sufficient for a defensible Layer 2 result. "
        "Reported descriptively to show whether the rubric items are stable "
        "across judges. Cohen κ interpretation (Landis & Koch): <0.20 poor, "
        "0.21–0.40 fair, 0.41–0.60 moderate, 0.61–0.80 substantial, "
        ">0.80 almost-perfect. The pre-registered Phase 1 threshold "
        "(κ_human–judge ≥ 0.6) does NOT apply here — this is judge-judge, "
        "not human–judge.\n"
    )
    if "error" in agreement:
        lines.append(f"\n_{agreement['error']}_\n")
    else:
        lines.append(
            f"\nJudges: **{' vs. '.join(agreement['judges'])}** · "
            f"common scored responses: {agreement['n_common_responses']}\n"
        )
        lines.append(
            f"\n**Overall (pooled across items):** "
            f"raw agreement {_fmt_pct(agreement['overall']['raw_agreement'])}, "
            f"Cohen κ {_fmt_num(agreement['overall']['cohens_kappa'])} "
            f"(n={agreement['overall']['n_pairs']} item-pairs).\n"
        )
        lines.append("\n| Item | n | Raw agreement | Cohen κ |\n")
        lines.append("|---|---|---|---|\n")
        for n in ITEM_NUMBERS:
            rec = agreement["per_item"].get(n, {})
            lines.append(
                f"| {n}. {ITEM_TITLES[n]} | {rec.get('n', 0)} "
                f"| {_fmt_pct(rec.get('raw_agreement'))} "
                f"| {_fmt_num(rec.get('cohens_kappa'))} |\n"
            )

    # 4. Length
    lines.append("\n## 4. Response length per condition (sanity check)\n")
    lines.append(
        "Length is a known judge-bias confound (longer answers often score "
        "higher regardless of content). If judge-framed responses are "
        "systematically longer than baseline, part of the framing delta is "
        "length-driven, not content-driven.\n"
    )
    lines.append("\n**By framing**\n\n| Framing | Mean chars | n |\n|---|---|---|\n")
    for k, rec in length["by_framing"].items():
        lines.append(f"| {k} | {_fmt_num(rec['mean_chars'], 0)} | {rec['n']} |\n")
    lines.append("\n**By model**\n\n| Model | Mean chars | n |\n|---|---|---|\n")
    for k, rec in length["by_model"].items():
        lines.append(f"| {k} | {_fmt_num(rec['mean_chars'], 0)} | {rec['n']} |\n")
    lines.append("\n**By prompt_id**\n\n| Prompt | Mean chars | n |\n|---|---|---|\n")
    for k, rec in length["by_prompt_id"].items():
        lines.append(f"| {k} | {_fmt_num(rec['mean_chars'], 0)} | {rec['n']} |\n")

    # 5. Self-preference
    lines.append("\n## 5. Self-preference floor check\n")
    lines.append(
        "Per Panickssery 2404.13076, LLM judges can systematically score their "
        "own outputs higher than other judges do. Per item, "
        "`self_mean − other_mean` on responses the judge itself authored. "
        "Magnitudes > 0.5 on multiple items are worth flagging.\n"
    )
    if not self_pref:
        lines.append("\n_No self-preference data (no judge appears as a response model)._\n")
    else:
        for judge, rec in self_pref.items():
            lines.append(
                f"\n### {judge} scoring its own responses "
                f"(vs. {rec['compared_against']}, n_authored={rec['n_authored_responses']})\n"
            )
            lines.append("| Item | Self mean | Other mean | Δ (self − other) |\n")
            lines.append("|---|---|---|---|\n")
            for n in ITEM_NUMBERS:
                row = rec["per_item"].get(n, {})
                lines.append(
                    f"| {n}. {ITEM_TITLES[n]} "
                    f"| {_fmt_num(row.get('self_mean'))} "
                    f"| {_fmt_num(row.get('other_mean'))} "
                    f"| {_fmt_num(row.get('delta'))} |\n"
                )

    lines.append("\n---\n")
    lines.append(
        "\n## What changes when the lawyer's scoring lands\n"
        "Replace the inter-judge κ table above with the κ_human–judge values "
        "per item. If the lawyer's scores diverge from the LLM judges on "
        "particular items, those items go on the rubric-revision list before "
        "the rubric is scaled to the other five roles.\n"
    )
    return "".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    configure_logging("INFO")
    if not RAW_PATH.exists():
        raise FileNotFoundError(
            f"{RAW_PATH} not found — run run_llm_judge.py first."
        )
    judge_rows = _read_jsonl(RAW_PATH)
    responses = _read_jsonl(RESPONSES_PATH) if RESPONSES_PATH.exists() else []

    logger.info(
        "loaded %d judge rows, %d responses", len(judge_rows), len(responses)
    )

    framing_delta = per_judge_framing_delta(judge_rows)
    baseline_q1 = per_model_baseline_q1(judge_rows)
    agreement = inter_judge_agreement(judge_rows)
    length = length_per_condition(responses)
    self_pref = self_preference(judge_rows)

    JSON_OUT.write_text(
        json.dumps(
            {
                "n_responses": len(responses),
                "n_judge_calls": len(judge_rows),
                "framing_delta": framing_delta,
                "baseline_q1": baseline_q1,
                "agreement": agreement,
                "length": length,
                "self_preference": self_pref,
            },
            indent=2,
            ensure_ascii=False,
        )
    )

    md = render_markdown(
        n_responses=len(responses),
        n_judge_calls=len(judge_rows),
        framing_delta=framing_delta,
        baseline_q1=baseline_q1,
        agreement=agreement,
        length=length,
        self_pref=self_pref,
    )
    MD_OUT.write_text(md)

    logger.info("wrote %s", MD_OUT)
    logger.info("wrote %s", JSON_OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
