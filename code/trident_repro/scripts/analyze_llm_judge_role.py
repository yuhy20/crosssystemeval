"""LLM-judge analysis — role-specific rubric (lawyer / doctor).

Reads `data/pilot/judge_v2/llm_judge_{rubric}_raw.jsonl` (40 rows: 2 judges ×
20 responses) and produces directional pilot signals against the role-rubric.

Outputs:
    data/pilot/judge_v2/llm_judge_{rubric}_analysis.md
    data/pilot/judge_v2/llm_judge_{rubric}_analysis.json

Mirrors the structure of `analyze_llm_judge.py` but is parameterized on the
target role (lawyer / doctor) — the "framing delta" axis compares baseline vs.
the target role's framing rather than baseline vs. judge.

Usage:
    cd code/trident_repro
    uv run python scripts/analyze_llm_judge_role.py --rubric lawyer
    uv run python scripts/analyze_llm_judge_role.py --rubric doctor
"""

from __future__ import annotations

import argparse
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

from rubric_data import RUBRIC_CONFIG  # noqa: E402

logger = logging.getLogger("crosssystemeval.llm_judge_role.analyze")

REPO_ROOT = SCRIPT_DIR.resolve().parents[2]
PILOT_DIR = REPO_ROOT / "data" / "pilot" / "judge_v2"
RESPONSES_PATH = PILOT_DIR / "responses.jsonl"


ITEM_NUMBERS = list(range(1, 11))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open() as f:
        for line in f:
            s = line.strip()
            if s:
                rows.append(json.loads(s))
    return rows


def _mean(xs: list[float]) -> float | None:
    return statistics.mean(xs) if xs else None


def _round(x: float | None, n: int = 2) -> float | None:
    return round(x, n) if x is not None else None


def cohens_kappa(a: list[int], b: list[int]) -> float | None:
    if len(a) != len(b) or not a:
        return None
    cats = sorted(set(a) | set(b))
    if len(cats) < 2:
        return 1.0 if all(x == y for x, y in zip(a, b)) else 0.0
    n = len(a)
    po = sum(1 for x, y in zip(a, b) if x == y) / n
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


def _score_for(row: dict, n: int) -> int | None:
    ps = row.get("parsed_scores") or {}
    rec = ps.get(str(n)) or ps.get(n)
    if isinstance(rec, dict):
        s = rec.get("score")
        if isinstance(s, int):
            return s
    return None


# ---------------------------------------------------------------------------
# Analyses
# ---------------------------------------------------------------------------


def per_judge_framing_delta(
    judge_rows: list[dict], role_framing: str
) -> dict:
    """Per-judge, per-item mean(role-framed) − mean(baseline)."""
    out: dict[str, dict[int, dict]] = defaultdict(dict)
    by_judge: dict[str, list[dict]] = defaultdict(list)
    for r in judge_rows:
        if r.get("parsed_scores"):
            by_judge[r["judge_model"]].append(r)

    for judge, rows in by_judge.items():
        for n in ITEM_NUMBERS:
            base = [
                _score_for(r, n)
                for r in rows
                if r["framing"] == "baseline" and _score_for(r, n) is not None
            ]
            role = [
                _score_for(r, n)
                for r in rows
                if r["framing"] == role_framing and _score_for(r, n) is not None
            ]
            base_m = _mean(base)
            role_m = _mean(role)
            delta = (
                role_m - base_m
                if (base_m is not None and role_m is not None)
                else None
            )
            out[judge][n] = {
                "baseline_mean": _round(base_m),
                "role_mean": _round(role_m),
                "delta": _round(delta),
                "n_baseline": len(base),
                "n_role": len(role),
            }
    return dict(out)


def per_model_baseline_q1(judge_rows: list[dict]) -> dict:
    """Per-(judge × response_model) mean rubric total on baseline_q1.

    Standard-bleed default-direction proxy: when no role is claimed, which
    model's response defaults closest to role-appropriate?
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


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def _fmt_num(x, n: int = 2) -> str:
    if x is None:
        return "—"
    if isinstance(x, int):
        return str(x)
    return f"{x:.{n}f}"


def render_markdown(
    *,
    rubric: str,
    role_framing: str,
    item_titles: dict[int, str],
    n_judge_calls: int,
    framing_delta: dict,
    baseline_q1: dict,
    agreement: dict,
) -> str:
    lines: list[str] = []
    lines.append(
        f"# LLM-as-judge pilot analysis — source-first {rubric} rubric\n"
    )
    lines.append(
        f"**Caveats first.** Run against the source-first {rubric} rubric "
        f"(`rubrics/{rubric}_v1_source_first.md`). The Layer 2 validation "
        "result (κ_human–judge ≥ 0.6 against an expert rater) is NOT yet in "
        f"hand for the {rubric} rubric — outreach packets drafted, expert "
        "scoring pending. Treat everything below as **directional pilot "
        "signals**, not validated ICR.\n"
    )
    lines.append(
        "Specifically, this analysis cannot tell you: (1) whether the judges "
        "agree with a human expert; (2) whether positive-content items and "
        "bleed-detection items load on a single latent variable (item-"
        "correlation matrix needs more cells than 20); (3) whether the "
        "rule-citation fidelity is substantively correct under NY-binding law.\n"
    )
    lines.append(
        "What it *can* tell you: direction of the role-claim manipulation, "
        f"cross-model baseline-default pattern, and inter-judge reliability "
        "of the rubric (descriptive).\n"
    )
    lines.append("---\n")
    lines.append(
        f"**Pilot:** 20 responses (baseline + {role_framing}, 5 models × 4 "
        f"prompts) · **Judge calls:** {n_judge_calls}\n"
    )

    # 1. Framing delta
    lines.append(
        f"\n## 1. Did the {role_framing} role claim move scores? "
        f"(per-judge baseline → {role_framing} delta)\n"
    )
    lines.append(
        f"Positive delta = scores rise when the user claims the {role_framing} "
        "role. Items 1–7/8 should rise (role-appropriate content increases); "
        "the bleed-detection items (8 or 9, 10) should be stable or rise "
        "slightly. If they move strongly together, role-claim and "
        "bleed-detection are confounded.\n"
    )
    for judge, items in framing_delta.items():
        lines.append(f"\n### Judge: {judge}\n")
        lines.append(
            f"| # | Item | Baseline mean | {role_framing.capitalize()} "
            "mean | Δ | n(base, role) |\n"
            "|---|---|---|---|---|---|"
        )
        for n in ITEM_NUMBERS:
            d = items.get(n, {})
            lines.append(
                f"| {n} | {item_titles.get(n, '?')} | "
                f"{_fmt_num(d.get('baseline_mean'))} | "
                f"{_fmt_num(d.get('role_mean'))} | "
                f"{_fmt_num(d.get('delta'))} | "
                f"({d.get('n_baseline', 0)}, {d.get('n_role', 0)}) |"
            )

    # 2. Baseline default
    lines.append(
        "\n\n## 2. Standard-bleed default-direction (per-judge × response_model "
        "baseline_q1 total / 30)\n"
    )
    lines.append(
        f"Higher total = the LLM brings {rubric}-appropriate content unprompted "
        "(\"standard bleed\" toward this role). Lower total = the LLM defaults "
        "elsewhere; the role frame would have to do all the work.\n"
    )
    for judge, by_model in baseline_q1.items():
        lines.append(f"\n### Judge: {judge}\n")
        lines.append("| Response model | Mean total /30 | n |\n|---|---|---|")
        for model, d in sorted(by_model.items()):
            lines.append(
                f"| {model} | {_fmt_num(d.get('mean_total_out_of_30'))} | "
                f"{d.get('n', 0)} |"
            )

    # 3. Inter-judge agreement
    lines.append("\n\n## 3. Inter-judge agreement (descriptive — 2 judges ≠ Layer 2)\n")
    if "error" in agreement:
        lines.append(f"_{agreement['error']}_\n")
    else:
        lines.append(
            f"**Judges:** {' / '.join(agreement['judges'])} · "
            f"**Common responses:** {agreement['n_common_responses']}\n"
        )
        lines.append("| # | Item | Raw agreement | Cohen κ | n |\n|---|---|---|---|---|")
        for n in ITEM_NUMBERS:
            d = agreement["per_item"].get(n, {})
            ra = d.get("raw_agreement")
            ra_pct = f"{ra * 100:.1f}%" if isinstance(ra, (int, float)) else "—"
            lines.append(
                f"| {n} | {item_titles.get(n, '?')} | {ra_pct} | "
                f"{_fmt_num(d.get('cohens_kappa'))} | {d.get('n', 0)} |"
            )
        ov = agreement["overall"]
        ov_ra = ov.get("raw_agreement")
        ov_ra_pct = f"{ov_ra * 100:.1f}%" if isinstance(ov_ra, (int, float)) else "—"
        lines.append(
            f"\n**Overall:** raw {ov_ra_pct} · κ "
            f"{_fmt_num(ov.get('cohens_kappa'))} · n={ov.get('n_pairs', 0)}\n"
        )

    lines.append("\n---\n")
    lines.append(
        "## What this analysis is NOT\n\n"
        f"- A claim that the {rubric} rubric is validated. Layer 3 (expert "
        "review) is pending.\n"
        "- A claim that the LLM-judge reliability transfers to human-rater "
        f"reliability. κ_judge–judge is **not** κ_human–judge.\n"
        "- A claim about statistical significance. With 20 responses per "
        "rubric, the cell counts are too small for confidence intervals; "
        "deltas are reported as directional only.\n"
        "- Self-preference is omitted here (a flagship-tier judge does not "
        "share family with all 5 response-models, so the symmetry the "
        "judge-rubric analysis exploited is not available; revisit when the "
        f"{rubric} rubric is rerun with response-model coverage that includes "
        "both judges).\n"
    )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--rubric",
        required=True,
        choices=sorted(RUBRIC_CONFIG.keys()),
        help="Which role-rubric analysis to run (lawyer or doctor).",
    )
    args = parser.parse_args()
    cfg = RUBRIC_CONFIG[args.rubric]
    rubric = args.rubric

    configure_logging("INFO")
    raw_path = PILOT_DIR / cfg["output"]
    if not raw_path.exists():
        logger.error("raw judge file not found: %s", raw_path)
        return 1

    judge_rows = _read_jsonl(raw_path)
    logger.info("loaded %d judge rows from %s", len(judge_rows), raw_path)

    # Pick the non-baseline framing as the role framing for delta analysis.
    role_framings = [f for f in cfg["framings"] if f != "baseline"]
    if len(role_framings) != 1:
        logger.error(
            "expected exactly one non-baseline framing in cfg; got %s",
            cfg["framings"],
        )
        return 1
    role_framing = role_framings[0]

    item_titles = {item["n"]: item["title"] for item in cfg["items"]}

    framing_delta = per_judge_framing_delta(judge_rows, role_framing)
    baseline_q1 = per_model_baseline_q1(judge_rows)
    agreement = inter_judge_agreement(judge_rows)

    md = render_markdown(
        rubric=rubric,
        role_framing=role_framing,
        item_titles=item_titles,
        n_judge_calls=len(judge_rows),
        framing_delta=framing_delta,
        baseline_q1=baseline_q1,
        agreement=agreement,
    )

    md_path = PILOT_DIR / f"llm_judge_{rubric}_analysis.md"
    json_path = PILOT_DIR / f"llm_judge_{rubric}_analysis.json"
    md_path.write_text(md)
    json_path.write_text(
        json.dumps(
            {
                "rubric": rubric,
                "role_framing": role_framing,
                "n_judge_calls": len(judge_rows),
                "framing_delta": framing_delta,
                "baseline_q1": baseline_q1,
                "inter_judge_agreement": agreement,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    logger.info("wrote %s", md_path)
    logger.info("wrote %s", json_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
