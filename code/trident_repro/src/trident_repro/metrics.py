"""Aggregation + inter-judge agreement metrics.

Avoids a numpy dependency: Cohen's kappa and Pearson r are implemented in
pure Python over small lists (N up to a few thousand is fine).
"""

from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from trident_repro.pipeline import RunRecord

# ---------------------------------------------------------------------------
# TRIDENT Figure 4 published means (approximate, hardcoded).
# Keyed by a substring of the target model name.
# ---------------------------------------------------------------------------

PUBLISHED_MEANS: dict[str, float] = {
    "gpt-4o": 1.4,
    "gemini-2.5-flash": 1.3,
    "claude-3-5-sonnet": 1.4,  # implicit GPT-4o-adjacent baseline
}

TOLERANCE: float = 0.3


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class DomainStats:
    domain: str
    n: int
    mean_score: float
    score_histogram: dict[int, int]


@dataclass(frozen=True, slots=True)
class AgreementStats:
    n: int
    cohen_kappa: float
    pearson_r: float
    exact_agreement_pct: float


@dataclass(frozen=True, slots=True)
class PublishedComparison:
    target_model: str
    observed_mean: float
    published_mean: float | None
    delta: float | None
    within_tolerance: bool


@dataclass(frozen=True, slots=True)
class Aggregate:
    total: int
    overall_mean: float
    per_domain: list[DomainStats] = field(default_factory=list)
    agreement: AgreementStats | None = None
    published: PublishedComparison | None = None


# ---------------------------------------------------------------------------
# IO
# ---------------------------------------------------------------------------


def load_records(path: Path) -> list[RunRecord]:
    """Load a run's JSONL into `RunRecord`s (skips blank lines)."""
    out: list[RunRecord] = []
    with path.open("r", encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line:
                continue
            out.append(RunRecord.model_validate_json(line))
    return out


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------


def _mean(values: Sequence[float]) -> float:
    if not values:
        return float("nan")
    return sum(values) / len(values)


def cohen_kappa(a: Sequence[int], b: Sequence[int]) -> float:
    """Unweighted Cohen's kappa over integer category labels.

    Returns `nan` on empty input. Returns 1.0 when observed == expected
    agreement at the degenerate ceiling (both raters identical, one class).
    """
    if len(a) != len(b):
        raise ValueError(f"length mismatch: {len(a)} vs {len(b)}")
    n = len(a)
    if n == 0:
        return float("nan")

    categories = sorted(set(a) | set(b))
    observed = sum(1 for x, y in zip(a, b, strict=True) if x == y) / n

    counts_a = Counter(a)
    counts_b = Counter(b)
    expected = sum((counts_a[c] / n) * (counts_b[c] / n) for c in categories)

    if math.isclose(expected, 1.0):
        return 1.0 if math.isclose(observed, 1.0) else 0.0
    return (observed - expected) / (1.0 - expected)


def pearson_r(a: Sequence[float], b: Sequence[float]) -> float:
    """Pearson correlation. Returns `nan` on <2 samples or zero variance."""
    if len(a) != len(b):
        raise ValueError(f"length mismatch: {len(a)} vs {len(b)}")
    n = len(a)
    if n < 2:
        return float("nan")

    mean_a = _mean(a)
    mean_b = _mean(b)
    num = sum((x - mean_a) * (y - mean_b) for x, y in zip(a, b, strict=True))
    den_a = math.sqrt(sum((x - mean_a) ** 2 for x in a))
    den_b = math.sqrt(sum((y - mean_b) ** 2 for y in b))
    if den_a == 0.0 or den_b == 0.0:
        return float("nan")
    return num / (den_a * den_b)


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------


def _per_domain(records: Iterable[RunRecord]) -> list[DomainStats]:
    buckets: dict[str, list[RunRecord]] = defaultdict(list)
    for r in records:
        buckets[r.domain].append(r)

    out: list[DomainStats] = []
    for domain, rows in sorted(buckets.items()):
        means = [r.mean_score for r in rows]
        hist: dict[int, int] = {}
        for r in rows:
            for s in (r.judge_a.score, r.judge_b.score):
                hist[s] = hist.get(s, 0) + 1
        out.append(
            DomainStats(
                domain=domain,
                n=len(rows),
                mean_score=_mean(means),
                score_histogram=dict(sorted(hist.items())),
            )
        )
    return out


def _agreement(records: Sequence[RunRecord]) -> AgreementStats | None:
    if not records:
        return None
    a = [r.judge_a.score for r in records]
    b = [r.judge_b.score for r in records]
    exact = sum(1 for x, y in zip(a, b, strict=True) if x == y) / len(records) * 100.0
    return AgreementStats(
        n=len(records),
        cohen_kappa=cohen_kappa(a, b),
        pearson_r=pearson_r([float(x) for x in a], [float(x) for x in b]),
        exact_agreement_pct=exact,
    )


def compare_to_published(target_model: str, observed_mean: float) -> PublishedComparison:
    """Match `target_model` to a published-mean key by substring (case-insensitive)."""
    key = target_model.lower()
    published: float | None = None
    for pattern, value in PUBLISHED_MEANS.items():
        if pattern in key:
            published = value
            break

    if published is None:
        return PublishedComparison(
            target_model=target_model,
            observed_mean=observed_mean,
            published_mean=None,
            delta=None,
            within_tolerance=False,
        )

    delta = observed_mean - published
    return PublishedComparison(
        target_model=target_model,
        observed_mean=observed_mean,
        published_mean=published,
        delta=delta,
        within_tolerance=abs(delta) <= TOLERANCE,
    )


def aggregate(records: Sequence[RunRecord]) -> Aggregate:
    """Full aggregation: per-domain + inter-judge agreement + published delta."""
    if not records:
        return Aggregate(total=0, overall_mean=float("nan"))

    target_model = records[0].target_model
    overall_mean = _mean([r.mean_score for r in records])
    return Aggregate(
        total=len(records),
        overall_mean=overall_mean,
        per_domain=_per_domain(records),
        agreement=_agreement(records),
        published=compare_to_published(target_model, overall_mean),
    )


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def format_report(agg: Aggregate) -> str:
    """Human-readable summary table for the CLI."""
    lines: list[str] = []
    lines.append(f"total records : {agg.total}")
    lines.append(f"overall mean  : {agg.overall_mean:.3f}")
    lines.append("")
    lines.append("per-domain:")
    lines.append(f"  {'domain':<10} {'n':>5} {'mean':>7}")
    for d in agg.per_domain:
        lines.append(f"  {d.domain:<10} {d.n:>5} {d.mean_score:>7.3f}")

    if agg.agreement is not None:
        a = agg.agreement
        lines.append("")
        lines.append("inter-judge agreement:")
        lines.append(f"  n                 : {a.n}")
        lines.append(f"  cohen_kappa       : {a.cohen_kappa:.3f}")
        lines.append(f"  pearson_r         : {a.pearson_r:.3f}")
        lines.append(f"  exact_agreement_% : {a.exact_agreement_pct:.1f}")

    if agg.published is not None:
        p = agg.published
        lines.append("")
        lines.append("vs. published (TRIDENT Fig. 4):")
        lines.append(f"  target_model     : {p.target_model}")
        lines.append(f"  observed_mean    : {p.observed_mean:.3f}")
        if p.published_mean is None:
            lines.append("  published_mean   : (no hardcoded entry for this model)")
        else:
            lines.append(f"  published_mean   : {p.published_mean:.3f}")
            assert p.delta is not None
            lines.append(f"  delta            : {p.delta:+.3f}")
            lines.append(
                f"  within_tolerance : {p.within_tolerance}  (|delta| <= {TOLERANCE})"
            )
    return "\n".join(lines)


def aggregate_to_json(agg: Aggregate) -> str:
    """Machine-readable dump (for notebooks / downstream tooling)."""
    payload = {
        "total": agg.total,
        "overall_mean": agg.overall_mean,
        "per_domain": [
            {
                "domain": d.domain,
                "n": d.n,
                "mean_score": d.mean_score,
                "score_histogram": d.score_histogram,
            }
            for d in agg.per_domain
        ],
        "agreement": (
            None
            if agg.agreement is None
            else {
                "n": agg.agreement.n,
                "cohen_kappa": agg.agreement.cohen_kappa,
                "pearson_r": agg.agreement.pearson_r,
                "exact_agreement_pct": agg.agreement.exact_agreement_pct,
            }
        ),
        "published": (
            None
            if agg.published is None
            else {
                "target_model": agg.published.target_model,
                "observed_mean": agg.published.observed_mean,
                "published_mean": agg.published.published_mean,
                "delta": agg.published.delta,
                "within_tolerance": agg.published.within_tolerance,
            }
        ),
    }
    return json.dumps(payload, indent=2, sort_keys=True)
