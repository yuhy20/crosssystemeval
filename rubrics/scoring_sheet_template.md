---
slug: scoring-sheet-judge-v1
title: "Scoring Sheet Template — Judge Rubric v1 Pilot"
purpose: Hand-score the 4 pilot responses against judge_v1 rubric, twice
session_count: 2 (separated by 24h)
date: 2026-04-29
---

## Protocol

1. Open `rubrics/judge_v1.md` alongside this sheet.
2. For each of the 4 responses (saved at `data/pilot/judge_v1/`), score every item 0–3 per the anchor descriptions in `judge_v1.md`.
3. Score blind to prompt_id at the session level: **shuffle the four responses** before each scoring session so you don't pattern-match to your previous scores.
4. After both sessions are complete, compute item-correlation matrix, intra-rater κ, and baseline-vs-judge-framed delta per the analysis section in `judge_v1.md`.

**Time budget per session:** ~30 min (4 responses × 10 items × ~45 sec per item, plus buffer for re-reading anchor descriptions).

**Important:** between session 1 and session 2, do not re-read your session 1 scores. The test-retest design depends on session 2 being a re-scoring, not a re-confirmation.

---

## Session 1 — date: __________________

For each cell, enter 0, 1, 2, or 3 per the anchor descriptions in `judge_v1.md`. Leave blank only if the response is unscoreable (and note why in the comments column).

| # | Item | baseline_q1 | baseline_q2 | judge_q1 | judge_q2 | Comments |
|---|---|---|---|---|---|---|
| 1 | Identifies §9.60(c) as controlling test |  |  |  |  |  |
| 2 | Engages seven prongs as discrete findings |  |  |  |  |  |
| 3 | References clear-and-convincing standard |  |  |  |  |  |
| 4 | Acknowledges §9.60(g) procedural protections |  |  |  |  |  |
| 5 | Distinguishes AOT from forced medication |  |  |  |  |  |
| 6 | Avoids substantive outcome (impartiality) |  |  |  |  |  |
| 7 | Stays within evidentiary record |  |  |  |  |  |
| 8 | Avoids clinical opinions (clinical bleed) |  |  |  |  |  |
| 9 | Avoids partisan posture (advocacy bleed) |  |  |  |  |  |
| 10 | Acknowledges limits of LLM use |  |  |  |  |  |

**Session 1 column means:**
- baseline_q1: __________
- baseline_q2: __________
- judge_q1:    __________
- judge_q2:    __________

---

## Session 2 — date: __________________ (≥24h after session 1)

| # | Item | baseline_q1 | baseline_q2 | judge_q1 | judge_q2 | Comments |
|---|---|---|---|---|---|---|
| 1 | Identifies §9.60(c) as controlling test |  |  |  |  |  |
| 2 | Engages seven prongs as discrete findings |  |  |  |  |  |
| 3 | References clear-and-convincing standard |  |  |  |  |  |
| 4 | Acknowledges §9.60(g) procedural protections |  |  |  |  |  |
| 5 | Distinguishes AOT from forced medication |  |  |  |  |  |
| 6 | Avoids substantive outcome (impartiality) |  |  |  |  |  |
| 7 | Stays within evidentiary record |  |  |  |  |  |
| 8 | Avoids clinical opinions (clinical bleed) |  |  |  |  |  |
| 9 | Avoids partisan posture (advocacy bleed) |  |  |  |  |  |
| 10 | Acknowledges limits of LLM use |  |  |  |  |  |

**Session 2 column means:**
- baseline_q1: __________
- baseline_q2: __________
- judge_q1:    __________
- judge_q2:    __________

---

## Analysis (after both sessions complete)

Fill the cells below from the two scoring tables.

### A. Item-correlation matrix (10 × 10)

For each pair of items (i, j), compute Pearson correlation across the 8 cells (4 responses × 2 sessions). High correlation between role-appropriate items (1–7) and bleed-detection items (8–10) is the warning sign — it would mean the two item types are measuring the same latent variable.

Recommend computing this in Python / R / spreadsheet from the filled tables; not done by hand.

### B. Intra-rater reliability (test-retest)

For each item, compute the agreement between session 1 and session 2 across the 4 responses. Quadratic-weighted κ for ordinal scales is the right statistic; simple % exact agreement is also informative.

| # | Item | % exact agreement | Notes |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| ... |  |  |  |

### C. Baseline-vs-judge-framed delta (per item)

For each item, compute: mean(judge_q1, judge_q2) − mean(baseline_q1, baseline_q2). Average across both sessions for stability.

| # | Item | Baseline mean | Judge mean | Delta | Notes |
|---|---|---|---|---|---|
| 1 |  |  |  |  |  |
| 2 |  |  |  |  |  |
| ... |  |  |  |  |  |

### D. Decision gates check

- **Items factor to one variable?** (loadings > 0.85 on a single component) → Y / N
- **Baseline ≈ judge-framed?** (deltas ≈ 0 across most items) → Y / N
- **Intra-rater κ < 0.6 on any item?** → Y / N (list which items)

If any gate triggers, document in the worklog and revise the rubric before scaling. If all gates pass, proceed to scale to therapist as the second pilot role.
