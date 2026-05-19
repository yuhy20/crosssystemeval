"""Build TypeScript chart-data module from v1 + v2 analysis JSONs.

Reads:
    data/pilot/judge_v2/llm_judge_lawyer_analysis.json      (v1)
    data/pilot/judge_v2/llm_judge_lawyer_v2_analysis.json   (v2)
    data/pilot/judge_v2/llm_judge_doctor_analysis.json      (v1)
    data/pilot/judge_v2/llm_judge_doctor_v2_analysis.json   (v2)
    data/pilot/judge_v2/llm_judge_judge_analysis.json       (single, v2-pattern)

Writes:
    ui/app/slides/_chartData.ts

Auto-generated so slide numbers are never hand-typed.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PKG_SRC = SCRIPT_DIR.parent / "src"
if str(PKG_SRC) not in sys.path:
    sys.path.insert(0, str(PKG_SRC))

from rubric_data import (  # noqa: E402
    LAWYER_RUBRIC_ITEMS,
    DOCTOR_RUBRIC_ITEMS,
    JUDGE_RUBRIC_ITEMS,
)

REPO_ROOT = SCRIPT_DIR.resolve().parents[2]
PILOT_DIR = REPO_ROOT / "data" / "pilot" / "judge_v2"
OUT_PATH = REPO_ROOT / "ui" / "app" / "slides" / "_chartData.ts"

# Short labels (Y-axis on charts) — kept under ~38 chars for visual budget.
LAWYER_SHORT_LABELS: dict[int, str] = {
    1: "Diligent advocacy (Rule 1.3)",
    2: "Client communication (Rule 1.4)",
    3: "Conventional relationship (1.14(a))",
    4: "Protective-action ceiling (1.14(b))",
    5: "Confidentiality (1.6(a) / 1.14(c))",
    6: "Self-harm exception (1.6(b)(1))",
    7: "Advisor function (Rule 2.1)",
    8: "Adversarial duty (Rule 3.1(a))",
    9: "No clinical-opinion bleed",
    10: "No AI-fabricated authority",
}
DOCTOR_SHORT_LABELS: dict[int, str] = {
    1: "Engage in decisions (Op. 2.1.2)",
    2: "Substituted-judgment (2.1.2(d))",
    3: "Best-interest fallback (2.1.2(e))",
    4: "Ethics-committee (2.1.2(f))",
    5: "Confidentiality (Op. 3.2.1)",
    6: "Paramount duty (Principle VIII)",
    7: "Competent care + PHL §230",
    8: "Does not adjudicate §9.60",
    9: "Not the patient's adversary",
    10: "No AI-fabricated clinical content",
}
JUDGE_SHORT_LABELS: dict[int, str] = {
    1: "§9.60(c) controlling test",
    2: "§9.60(c)(1)–(7) prongs",
    3: "Clear-and-convincing (§9.60(j))",
    4: "Counsel + right to be heard",
    5: "AOT ≠ forced medication",
    6: "Impartiality (Rule 2.2)",
    7: "Record-bound (Rule 2.9(C))",
    8: "No clinical-opinion bleed",
    9: "No advocacy-posture bleed",
    10: "No AI-fabricated authority",
}

BLEED_ITEMS = {"lawyer": [9, 10], "doctor": [8, 9, 10], "judge": [8, 9, 10]}


def _load(name: str) -> dict | None:
    p = PILOT_DIR / name
    if not p.exists():
        return None
    return json.loads(p.read_text())


def _delta_rows(analysis: dict) -> dict[str, dict[int, float]]:
    """Return {judge_model: {item_n: delta}}."""
    fd = analysis["framing_delta"]
    return {
        judge: {int(n): float(v["delta"]) for n, v in items.items()}
        for judge, items in fd.items()
    }


def _kappa_rows(analysis: dict) -> dict[int, float]:
    return {
        int(n): float(v["cohens_kappa"])
        for n, v in analysis["inter_judge_agreement"]["per_item"].items()
    }


def _build_rubric_payload(
    rubric: str,
    labels: dict[int, str],
    v1_analysis: dict,
    v2_analysis: dict | None,
) -> dict:
    items_meta = [
        {"n": n, "label": labels[n], "isBleed": n in BLEED_ITEMS[rubric]}
        for n in sorted(labels.keys())
    ]
    v1_deltas = _delta_rows(v1_analysis)
    v1_kappa = _kappa_rows(v1_analysis)
    payload = {
        "rubric": rubric,
        "items": items_meta,
        "judges": list(v1_deltas.keys()),
        "v1": {
            "deltas": v1_deltas,
            "kappa": v1_kappa,
            "overall_kappa": v1_analysis["inter_judge_agreement"]
            .get("overall", {})
            .get("cohens_kappa"),
        },
    }
    if v2_analysis is not None:
        v2_deltas = _delta_rows(v2_analysis)
        v2_kappa = _kappa_rows(v2_analysis)
        payload["v2"] = {
            "deltas": v2_deltas,
            "kappa": v2_kappa,
            "overall_kappa": v2_analysis["inter_judge_agreement"]
            .get("overall", {})
            .get("cohens_kappa"),
        }
    return payload


def _ts_literal(obj) -> str:
    """JSON encode with TS-style indentation."""
    return json.dumps(obj, indent=2, ensure_ascii=False)


def main() -> int:
    lawyer_v1 = _load("llm_judge_lawyer_analysis.json")
    lawyer_v2 = _load("llm_judge_lawyer_v2_analysis.json")
    doctor_v1 = _load("llm_judge_doctor_analysis.json")
    doctor_v2 = _load("llm_judge_doctor_v2_analysis.json")
    judge_only = _load("llm_judge_judge_analysis.json")
    if lawyer_v1 is None or doctor_v1 is None:
        print("missing v1 analysis files", file=sys.stderr)
        return 1

    lawyer = _build_rubric_payload(
        "lawyer", LAWYER_SHORT_LABELS, lawyer_v1, lawyer_v2
    )
    doctor = _build_rubric_payload(
        "doctor", DOCTOR_SHORT_LABELS, doctor_v1, doctor_v2
    )
    judge = (
        _build_rubric_payload("judge", JUDGE_SHORT_LABELS, judge_only, None)
        if judge_only is not None
        else None
    )

    has_v2 = lawyer_v2 is not None and doctor_v2 is not None
    judge_export = (
        f"export const JUDGE: RubricPayload = {_ts_literal(judge)};\n"
        if judge is not None
        else "export const JUDGE: RubricPayload | null = null;\n"
    )
    ts = (
        "// AUTO-GENERATED by scripts/build_slide_chart_data.py.\n"
        "// Numbers come from data/pilot/judge_v2/llm_judge_*_analysis.json.\n"
        "// Re-run the generator after re-judging to refresh.\n\n"
        "export type ChartItem = { n: number; label: string; isBleed: boolean };\n"
        "export type RubricPayload = {\n"
        "  rubric: 'lawyer' | 'doctor' | 'judge';\n"
        "  items: ChartItem[];\n"
        "  judges: string[];\n"
        "  v1: {\n"
        "    deltas: Record<string, Record<string, number>>;\n"
        "    kappa: Record<string, number>;\n"
        "    overall_kappa: number | null;\n"
        "  };\n"
        "  v2?: {\n"
        "    deltas: Record<string, Record<string, number>>;\n"
        "    kappa: Record<string, number>;\n"
        "    overall_kappa: number | null;\n"
        "  };\n"
        "};\n\n"
        f"export const HAS_V2 = {str(has_v2).lower()};\n\n"
        f"export const LAWYER: RubricPayload = {_ts_literal(lawyer)};\n\n"
        f"export const DOCTOR: RubricPayload = {_ts_literal(doctor)};\n\n"
        f"{judge_export}"
    )
    OUT_PATH.write_text(ts)
    print(f"wrote {OUT_PATH} (v2_present={has_v2}, judge_present={judge is not None})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
