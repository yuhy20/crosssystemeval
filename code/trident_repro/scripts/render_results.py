"""Render calibration results as PNG + JSON for the UI.

Reads every `outputs/*.jsonl` run file, aggregates, and produces:

    ui/public/trident/
        ├── calibration_chart.png   # Apple-dark-themed bar chart
        └── results.json            # machine-readable table

Intended to be idempotent: run it after any new `trident-repro run`.

Usage:
    python scripts/render_results.py
"""

from __future__ import annotations

import json
import logging
import math
import sys
import warnings
from pathlib import Path


def _clean(value: float | None) -> float | None:
    """Return None for NaN/inf; otherwise the value. Keeps results.json valid JSON."""
    if value is None:
        return None
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value

import matplotlib as mpl
import matplotlib.pyplot as plt

# Silence findfont warnings when our preferred system font isn't installed.
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
warnings.filterwarnings("ignore", message="findfont.*")

ROOT = Path(__file__).resolve().parent.parent
UI_DIR = ROOT.parent.parent / "ui"
OUTPUTS = ROOT / "outputs"
DEST_DIR = UI_DIR / "public" / "trident"

# Ensure we can import the package without installing.
sys.path.insert(0, str(ROOT / "src"))
from trident_repro.metrics import aggregate, load_records  # noqa: E402

# ---------------------------------------------------------------------------
# Apple-dark styling
# ---------------------------------------------------------------------------

DARK_BG = "#0a0a0c"
CARD_BG = "#161618"
INK = "#f5f5f7"
INK_MUTED = "#a1a1a6"
HAIRLINE = "#2c2c2e"
ACCENT = "#0a84ff"
REF_GREY = "#a1a1a6"
BAND_GREEN = "#30d158"

mpl.rcParams.update(
    {
        "figure.facecolor": CARD_BG,
        "axes.facecolor": CARD_BG,
        "axes.edgecolor": HAIRLINE,
        "axes.labelcolor": INK_MUTED,
        "axes.titlecolor": INK,
        "axes.titlesize": 13,
        "axes.titleweight": "600",
        "axes.titlepad": 14,
        "xtick.color": INK_MUTED,
        "ytick.color": INK_MUTED,
        "grid.color": HAIRLINE,
        "grid.alpha": 0.6,
        "text.color": INK,
        "font.family": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 10.5,
        "axes.spines.top": False,
        "axes.spines.right": False,
    }
)

TOLERANCE = 0.3


# ---------------------------------------------------------------------------
# Build rows
# ---------------------------------------------------------------------------


def main() -> None:
    if not OUTPUTS.exists():
        raise SystemExit(f"No outputs directory at {OUTPUTS}")

    run_files = sorted(OUTPUTS.glob("*.jsonl"))
    if not run_files:
        raise SystemExit("No run files found. Execute trident-repro first.")

    rows = []
    for path in run_files:
        records = load_records(path)
        if not records:
            continue
        agg = aggregate(records)
        p = agg.published
        published_mean = p.published_mean if p is not None else None
        within = bool(p.within_tolerance) if p is not None else False
        rows.append(
            {
                "run": path.stem,
                "target_model": records[0].target_model,
                "n": agg.total,
                "observed_mean": round(agg.overall_mean, 3),
                "published_mean": published_mean,
                "delta": round(p.delta, 3) if (p and p.delta is not None) else None,
                "within_tolerance": within if published_mean is not None else None,
                "judge_a": records[0].judge_a.model,
                "judge_b": records[0].judge_b.model,
                "cohen_kappa": (
                    _clean(round(agg.agreement.cohen_kappa, 3))
                    if agg.agreement is not None
                    else None
                ),
                "pearson_r": (
                    _clean(round(agg.agreement.pearson_r, 3))
                    if agg.agreement is not None
                    else None
                ),
                "exact_agreement_pct": (
                    _clean(round(agg.agreement.exact_agreement_pct, 1))
                    if agg.agreement is not None
                    else None
                ),
                "verdict": (
                    "PASS"
                    if (p is not None and p.published_mean is not None and p.within_tolerance)
                    else (
                        "FAIL"
                        if (p is not None and p.published_mean is not None and not p.within_tolerance)
                        else "N/A"
                    )
                ),
            }
        )

    if not rows:
        raise SystemExit("No non-empty run files.")

    paired = [r for r in rows if r["published_mean"] is not None]
    unpaired = [r for r in rows if r["published_mean"] is None]

    # Sort each bucket for stable rendering: safest first (lowest observed).
    paired.sort(key=lambda r: r["observed_mean"])
    unpaired.sort(key=lambda r: r["observed_mean"])

    DEST_DIR.mkdir(parents=True, exist_ok=True)

    # -----------------------------------------------------------------------
    # Figure
    # -----------------------------------------------------------------------
    fig, axes = plt.subplots(
        1, 2, figsize=(13, 5.2), gridspec_kw={"width_ratios": [max(1, len(paired)), max(1, len(unpaired))]}
    )
    ax_p, ax_u = axes

    def _style_axis(ax: mpl.axes.Axes) -> None:
        ax.set_ylim(0, 5)
        ax.grid(axis="y", alpha=0.35)
        ax.set_ylabel("Harmfulness score (1 safe → 5 unsafe)")

    # --- left: paired ---
    if paired:
        labels = [r["target_model"] for r in paired]
        observed = [r["observed_mean"] for r in paired]
        published = [r["published_mean"] for r in paired]
        x = list(range(len(labels)))
        width = 0.38
        ax_p.bar(
            [i - width / 2 for i in x],
            observed,
            width=width,
            label="observed",
            color=ACCENT,
            edgecolor="none",
        )
        ax_p.bar(
            [i + width / 2 for i in x],
            published,
            width=width,
            label="TRIDENT published",
            color=REF_GREY,
            edgecolor="none",
        )
        for i, p in enumerate(published):
            if p is None:
                continue
            ax_p.fill_betweenx(
                [p - TOLERANCE, p + TOLERANCE],
                i - 0.5,
                i + 0.5,
                alpha=0.14,
                color=BAND_GREEN,
            )
        # Bar labels
        for i, v in enumerate(observed):
            ax_p.text(i - width / 2, v + 0.08, f"{v:.3f}", ha="center", color=INK, fontsize=9)
        for i, v in enumerate(published):
            ax_p.text(i + width / 2, v + 0.08, f"{v:.3f}", ha="center", color=INK_MUTED, fontsize=9)
        ax_p.set_xticks(x)
        ax_p.set_xticklabels(labels, rotation=12, ha="right")
        ax_p.set_title(f"vs. TRIDENT published (±{TOLERANCE} band)")
        ax_p.legend(loc="upper left", frameon=False, labelcolor=INK)
    else:
        ax_p.text(
            0.5, 0.5, "No runs matched a published mean",
            ha="center", va="center", transform=ax_p.transAxes, color=INK_MUTED,
        )
        ax_p.set_title("vs. TRIDENT published")
    _style_axis(ax_p)

    # --- right: unpaired ---
    if unpaired:
        labels = [r["target_model"] for r in unpaired]
        observed = [r["observed_mean"] for r in unpaired]
        x = list(range(len(labels)))
        ax_u.bar(x, observed, width=0.5, color=ACCENT, edgecolor="none")
        for i, v in enumerate(observed):
            ax_u.text(i, v + 0.08, f"{v:.3f}", ha="center", color=INK, fontsize=9)
        ax_u.set_xticks(x)
        ax_u.set_xticklabels(labels, rotation=12, ha="right")
        ax_u.set_title("Observed (no TRIDENT reference)")
    else:
        ax_u.text(
            0.5, 0.5, "All runs matched a published mean",
            ha="center", va="center", transform=ax_u.transAxes, color=INK_MUTED,
        )
        ax_u.set_title("Observed (no TRIDENT reference)")
    _style_axis(ax_u)

    fig.suptitle(
        "CrossSystemEval — Calibration (law domain, n=30, seed=42)",
        color=INK,
        fontsize=14,
        fontweight="600",
        y=0.995,
    )
    plt.tight_layout(rect=(0, 0, 1, 0.96))

    png_path = DEST_DIR / "calibration_chart.png"
    fig.savefig(png_path, dpi=200, facecolor=CARD_BG, bbox_inches="tight")
    plt.close(fig)

    # -----------------------------------------------------------------------
    # JSON
    # -----------------------------------------------------------------------
    payload = {
        "generated_at_rows": len(rows),
        "tolerance": TOLERANCE,
        "rows": rows,
    }
    (DEST_DIR / "results.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print(f"wrote {png_path}")
    print(f"wrote {DEST_DIR / 'results.json'}")


if __name__ == "__main__":
    main()
