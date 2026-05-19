"""Inter-coder-reliability (ICR) computation module — CrossSystemEval.

Computes per-item and pooled agreement between two raters scoring the same
items on a 0-3 ordinal scale. Designed to reproduce section 3
("Inter-judge agreement") of `data/pilot/judge_v2/llm_judge_analysis.md`
for any new pair of raters (LLM judge vs. LLM judge, or human vs. LLM judge).

Cohen's kappa (Cohen 1960, "A coefficient of agreement for nominal scales",
Educational and Psychological Measurement, 20(1): 37-46):

    κ = (p_o − p_e) / (1 − p_e)

where p_o is the observed proportion of agreements and p_e is the proportion
expected by chance under independence of the two raters' marginal
distributions.

Krippendorff's alpha (interval level, appropriate for 0-3 ordinal scores
where rater drift by one rung is "less wrong" than drift by three):

    α = 1 − D_o / D_e

with disagreement aggregated using squared-difference distances.

Pure-stdlib + numpy. No exotic deps.

CLI:
    python code/icr.py \\
        --scoring-sheets data/pilot/judge_v2/scoring_session_1 \\
        --llm-judge-jsonl data/pilot/judge_v2/llm_judge_raw.jsonl \\
        --output icr_report.md

The CLI compares (a) the two LLM judges against each other (default; pass
only --llm-judge-jsonl) or (b) the human scoring sheets against one named
LLM judge (pass --scoring-sheets and --llm-judge-jsonl together; the human
sheets are treated as rater A, the LLM judge as rater B).
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Iterable

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
# Core statistics
# ---------------------------------------------------------------------------


def percent_agreement(rater_a: list[int], rater_b: list[int]) -> float | None:
    """Raw observed-agreement proportion between two parallel rating lists.

    Returns None for empty / length-mismatched inputs.
    """
    if len(rater_a) != len(rater_b) or not rater_a:
        return None
    return sum(1 for x, y in zip(rater_a, rater_b) if x == y) / len(rater_a)


def cohen_kappa(rater_a: list[int], rater_b: list[int]) -> float | None:
    """Cohen's κ for two parallel rating lists (categories 0..3).

    Formula:
        κ = (p_o − p_e) / (1 − p_e)
    where p_o is observed agreement and p_e is expected-by-chance agreement
    from each rater's marginal category distribution. Cohen (1960).

    Returns None for empty / length-mismatched inputs. Returns 1.0 when both
    raters used a single (identical) category — κ is technically undefined
    in that degenerate case; the perfect-agreement limit matches the raw %.
    """
    if len(rater_a) != len(rater_b) or not rater_a:
        return None
    cats = sorted(set(rater_a) | set(rater_b))
    n = len(rater_a)
    p_o = sum(1 for x, y in zip(rater_a, rater_b) if x == y) / n
    if len(cats) < 2:
        return 1.0 if p_o >= 1.0 else 0.0
    pa = {c: rater_a.count(c) / n for c in cats}
    pb = {c: rater_b.count(c) / n for c in cats}
    p_e = sum(pa[c] * pb[c] for c in cats)
    if p_e >= 1.0:
        return 1.0 if p_o >= 1.0 else 0.0
    return (p_o - p_e) / (1.0 - p_e)


def krippendorff_alpha(ratings_matrix: list[list[int | None]]) -> float | None:
    """Krippendorff's α for ordinal/interval 0-3 ratings.

    ratings_matrix is shape (n_raters, n_items); cell value is the score
    that rater r assigned to item i, or None if missing.

    Uses interval-level distance δ²(c1, c2) = (c1 − c2)².

    Returns None if there are fewer than two valid pairable observations.
    """
    if not ratings_matrix or len(ratings_matrix) < 2:
        return None
    n_items = len(ratings_matrix[0])
    if any(len(row) != n_items for row in ratings_matrix):
        raise ValueError("all rater rows must have identical length")

    # Per-unit (item) values list, dropping missing entries.
    units: list[list[int]] = []
    for i in range(n_items):
        col = [row[i] for row in ratings_matrix if row[i] is not None]
        if len(col) >= 2:
            units.append(col)

    if not units:
        return None

    # Observed disagreement D_o: average pairwise squared difference within
    # units, weighted by 1/(m_u − 1) where m_u is the number of raters on u.
    num_o = 0.0
    n_pairable = 0
    for col in units:
        m = len(col)
        weight = 1.0 / (m - 1)
        for i in range(m):
            for j in range(m):
                if i != j:
                    num_o += weight * (col[i] - col[j]) ** 2
        n_pairable += m

    # Expected disagreement D_e: pairwise squared differences across ALL
    # values pooled, normalised by n*(n-1).
    pooled = [v for col in units for v in col]
    n = len(pooled)
    if n < 2:
        return None
    num_e = 0.0
    for i in range(n):
        for j in range(n):
            if i != j:
                num_e += (pooled[i] - pooled[j]) ** 2

    if num_e == 0:
        return 1.0 if num_o == 0 else 0.0
    # Both numerators are sums of m*(m-1) squared deltas in the standard
    # Krippendorff formulation; α = 1 − ((n − 1) * D_o_sum) / D_e_sum
    # where D_o_sum is the weighted observed sum and D_e_sum the pooled sum.
    return 1.0 - ((n - 1) * num_o) / num_e


def per_item_table(
    rater_a_by_item: dict[int, list[int]],
    rater_b_by_item: dict[int, list[int]],
    item_titles: dict[int, str] | None = None,
) -> list[dict]:
    """Return a list of dicts {item_id, n, raw_agreement, kappa} per item.

    Each item's two score lists must be parallel and same-length.
    """
    if item_titles is None:
        item_titles = ITEM_TITLES
    rows = []
    for item_id in sorted(set(rater_a_by_item) & set(rater_b_by_item)):
        a = rater_a_by_item[item_id]
        b = rater_b_by_item[item_id]
        rows.append(
            {
                "item_id": item_id,
                "title": item_titles.get(item_id, ""),
                "n": len(a),
                "raw_agreement": percent_agreement(a, b),
                "kappa": cohen_kappa(a, b),
            }
        )
    return rows


# ---------------------------------------------------------------------------
# Input loaders
# ---------------------------------------------------------------------------


_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
_INLINE_SCORE_RE = re.compile(
    r"###\s*Item\s+(\d+)\b.*?\*\*Score\s*\([^)]*\):\*\*\s*([0-3])\b",
    re.DOTALL,
)
_RESPONSE_FIELD_RE = re.compile(r"\*\*Response:\*\*\s*(response_\d+)")


def _parse_yaml_scalar(value: str) -> int | str:
    v = value.strip().strip('"').strip("'")
    try:
        return int(v)
    except ValueError:
        return v


def parse_scoring_sheet(path: Path) -> dict | None:
    """Parse one human scoring-sheet markdown into {response_id, scores}.

    Supports two score formats:
      1. YAML frontmatter at top of file with keys `response`, `item_1` ... `item_10`.
      2. Inline `### Item N. ...` blocks containing `**Score (0 / 1 / 2 / 3):** N`.

    Returns None if no scores were found (blank template).
    """
    text = path.read_text()
    response_id = path.stem
    scores: dict[int, int] = {}

    m = _FRONTMATTER_RE.match(text)
    if m:
        for line in m.group(1).splitlines():
            if ":" not in line:
                continue
            key, _, value = line.partition(":")
            key = key.strip()
            parsed = _parse_yaml_scalar(value)
            if key == "response" and isinstance(parsed, str):
                response_id = parsed
            elif key.startswith("item_") and isinstance(parsed, int):
                try:
                    n = int(key.split("_", 1)[1])
                except ValueError:
                    continue
                if 0 <= parsed <= 3:
                    scores[n] = parsed

    if not scores:
        rm = _RESPONSE_FIELD_RE.search(text)
        if rm:
            response_id = rm.group(1)
        for m in _INLINE_SCORE_RE.finditer(text):
            n = int(m.group(1))
            scores[n] = int(m.group(2))

    if not scores:
        return None
    return {"response_id": response_id, "scores": scores}


def load_scoring_sheets(directory: Path) -> dict[str, dict[int, int]]:
    """Load all response_NN.md scoring sheets in a directory.

    Returns {response_id: {item_n: score}}.
    """
    out: dict[str, dict[int, int]] = {}
    for path in sorted(directory.glob("response_*.md")):
        parsed = parse_scoring_sheet(path)
        if parsed is None:
            continue
        out[parsed["response_id"]] = parsed["scores"]
    return out


def load_llm_judge_rows(path: Path) -> list[dict]:
    """Load and lightly normalise an llm_judge_raw.jsonl file."""
    rows = []
    with path.open() as f:
        for line in f:
            s = line.strip()
            if s:
                rows.append(json.loads(s))
    return rows


def _score_for(row: dict, item_n: int) -> int | None:
    parsed = row.get("parsed_scores") or {}
    rec = parsed.get(str(item_n)) or parsed.get(item_n)
    if not rec:
        return None
    return rec.get("score")


def llm_judge_scores_by_response(
    rows: list[dict], judge_model: str
) -> dict[str, dict[int, int]]:
    """Index one judge's scores by response_id (e.g. 'response_01')."""
    out: dict[str, dict[int, int]] = {}
    for r in rows:
        if r.get("judge_model") != judge_model or not r.get("parsed_scores"):
            continue
        # Match analyze_llm_judge.py convention: response_idx 0 -> response_01
        rid = f"response_{int(r['response_idx']) + 1:02d}"
        out[rid] = {
            n: s for n in ITEM_NUMBERS if (s := _score_for(r, n)) is not None
        }
    return out


# ---------------------------------------------------------------------------
# Pair → per-item lists
# ---------------------------------------------------------------------------


def align_raters(
    a_by_response: dict[str, dict[int, int]],
    b_by_response: dict[str, dict[int, int]],
) -> tuple[dict[int, list[int]], dict[int, list[int]], list[str]]:
    """Build parallel per-item score lists over responses scored by both raters.

    Returns (rater_a_by_item, rater_b_by_item, ordered_response_ids).
    """
    common = sorted(set(a_by_response) & set(b_by_response))
    a_out: dict[int, list[int]] = defaultdict(list)
    b_out: dict[int, list[int]] = defaultdict(list)
    for rid in common:
        for n in ITEM_NUMBERS:
            sa = a_by_response[rid].get(n)
            sb = b_by_response[rid].get(n)
            if sa is None or sb is None:
                continue
            a_out[n].append(sa)
            b_out[n].append(sb)
    return dict(a_out), dict(b_out), common


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def _fmt_pct(v: float | None) -> str:
    return "—" if v is None else f"{v * 100:.1f}%"


def _fmt_num(v: float | None, n: int = 2) -> str:
    return "—" if v is None else f"{v:.{n}f}"


def render_markdown(
    rater_a_name: str,
    rater_b_name: str,
    n_common: int,
    per_item: list[dict],
    overall_raw: float | None,
    overall_kappa: float | None,
    n_pairs: int,
    alpha: float | None = None,
) -> str:
    lines = []
    lines.append("## 3. Inter-judge agreement (descriptive — NOT a validation result)\n")
    lines.append(
        "Two judges is **not** sufficient for a defensible Layer 2 result. "
        "Reported descriptively. With v2 anchors verbatim-quoting the source "
        "clause, ambiguity should be lower than v1 — but the comparison is "
        "directional, not statistical.\n"
    )
    lines.append(
        f"\nJudges: **{rater_a_name} vs. {rater_b_name}** · "
        f"common scored responses: {n_common}\n"
    )
    overall_line = (
        f"\n**Overall (pooled across items):** raw agreement "
        f"{_fmt_pct(overall_raw)}, Cohen κ {_fmt_num(overall_kappa)} "
        f"(n={n_pairs} item-pairs)"
    )
    if alpha is not None:
        overall_line += f"; Krippendorff α (interval) {_fmt_num(alpha)}"
    overall_line += ".\n"
    lines.append(overall_line)

    lines.append("\n| Item | n | Raw agreement | Cohen κ |\n")
    lines.append("|---|---|---|---|\n")
    for row in per_item:
        title = ITEM_TITLES.get(row["item_id"], row.get("title", ""))
        lines.append(
            f"| {row['item_id']}. {title} | {row['n']} | "
            f"{_fmt_pct(row['raw_agreement'])} | {_fmt_num(row['kappa'])} |\n"
        )
    return "".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _build_pair_from_inputs(
    scoring_sheets_dir: Path | None,
    llm_judge_jsonl: Path,
    judge_a: str | None,
    judge_b: str | None,
) -> tuple[str, str, dict[str, dict[int, int]], dict[str, dict[int, int]]]:
    """Return (name_a, name_b, scores_a, scores_b) for the comparison."""
    rows = load_llm_judge_rows(llm_judge_jsonl)
    judges_in_file = sorted({r["judge_model"] for r in rows})

    if scoring_sheets_dir is not None:
        a_scores = load_scoring_sheets(scoring_sheets_dir)
        if not a_scores:
            raise SystemExit(
                f"No scored sheets found in {scoring_sheets_dir} "
                "(template-only sheets are skipped)."
            )
        judge_choice = judge_b or (judges_in_file[0] if judges_in_file else None)
        if judge_choice is None:
            raise SystemExit("No judges present in llm_judge_raw.jsonl.")
        b_scores = llm_judge_scores_by_response(rows, judge_choice)
        return (
            scoring_sheets_dir.name,
            judge_choice,
            a_scores,
            b_scores,
        )

    # No human sheets: compare the two LLM judges in the file.
    if len(judges_in_file) < 2:
        raise SystemExit(
            f"Need ≥2 distinct judge_model values in {llm_judge_jsonl}; "
            f"found {judges_in_file}."
        )
    a_name = judge_a or judges_in_file[0]
    b_name = judge_b or next(j for j in judges_in_file if j != a_name)
    return (
        a_name,
        b_name,
        llm_judge_scores_by_response(rows, a_name),
        llm_judge_scores_by_response(rows, b_name),
    )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Compute Cohen κ, Krippendorff α, and raw agreement "
        "between two raters scoring the CrossSystemEval judge rubric."
    )
    p.add_argument(
        "--scoring-sheets",
        type=Path,
        default=None,
        help="Directory of human scoring-sheet markdowns "
        "(data/pilot/judge_v2/scoring_session_1). If omitted, both raters "
        "come from --llm-judge-jsonl.",
    )
    p.add_argument(
        "--llm-judge-jsonl",
        type=Path,
        required=True,
        help="Path to llm_judge_raw.jsonl.",
    )
    p.add_argument(
        "--judge-a",
        default=None,
        help="When comparing two LLM judges, name of rater A "
        "(default: first judge_model encountered).",
    )
    p.add_argument(
        "--judge-b",
        default=None,
        help="Name of rater B / the LLM judge to compare against the "
        "human sheets.",
    )
    p.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Path to write the markdown report to.",
    )
    args = p.parse_args(argv)

    name_a, name_b, scores_a, scores_b = _build_pair_from_inputs(
        args.scoring_sheets,
        args.llm_judge_jsonl,
        args.judge_a,
        args.judge_b,
    )

    a_by_item, b_by_item, common = align_raters(scores_a, scores_b)
    per_item = per_item_table(a_by_item, b_by_item)

    pooled_a: list[int] = []
    pooled_b: list[int] = []
    for n in ITEM_NUMBERS:
        pooled_a.extend(a_by_item.get(n, []))
        pooled_b.extend(b_by_item.get(n, []))

    overall_raw = percent_agreement(pooled_a, pooled_b)
    overall_kappa = cohen_kappa(pooled_a, pooled_b)
    alpha = krippendorff_alpha([pooled_a, pooled_b]) if pooled_a else None

    md = render_markdown(
        rater_a_name=name_a,
        rater_b_name=name_b,
        n_common=len(common),
        per_item=per_item,
        overall_raw=overall_raw,
        overall_kappa=overall_kappa,
        n_pairs=len(pooled_a),
        alpha=alpha,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(md)
    print(f"Wrote {args.output} ({len(common)} common responses; "
          f"{len(pooled_a)} item-pairs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
