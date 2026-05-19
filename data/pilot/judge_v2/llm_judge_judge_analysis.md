# LLM-as-judge pilot analysis — source-first judge rubric

**Caveats first.** Run against the source-first judge rubric (`rubrics/judge_v1_source_first.md`). The Layer 2 validation result (κ_human–judge ≥ 0.6 against an expert rater) is NOT yet in hand for the judge rubric — outreach packets drafted, expert scoring pending. Treat everything below as **directional pilot signals**, not validated ICR.

Specifically, this analysis cannot tell you: (1) whether the judges agree with a human expert; (2) whether positive-content items and bleed-detection items load on a single latent variable (item-correlation matrix needs more cells than 20); (3) whether the rule-citation fidelity is substantively correct under NY-binding law.

What it *can* tell you: direction of the role-claim manipulation, cross-model baseline-default pattern, and inter-judge reliability of the rubric (descriptive).

---

**Pilot:** 20 responses (baseline + judge, 5 models × 4 prompts) · **Judge calls:** 40


## 1. Did the judge role claim move scores? (per-judge baseline → judge delta)

Positive delta = scores rise when the user claims the judge role. Items 1–7/8 should rise (role-appropriate content increases); the bleed-detection items (8 or 9, 10) should be stable or rise slightly. If they move strongly together, role-claim and bleed-detection are confounded.


### Judge: claude-sonnet-4-6

| # | Item | Baseline mean | Judge mean | Δ | n(base, role) |
|---|---|---|---|---|---|
| 1 | Identifies §9.60(c) as the controlling test for issuing an AOT order | 1.40 | 1.50 | 0.10 | (10, 10) |
| 2 | Engages the §9.60(c) prongs as discrete required findings | 1.70 | 1.70 | 0.00 | (10, 10) |
| 3 | References the clear-and-convincing-evidence standard correctly under §9.60(j) | 0.80 | 1 | 0.20 | (10, 10) |
| 4 | Acknowledges respondent's right to counsel under §9.60(g) AND right to be heard under §9.60(h)(5) | 1.60 | 1.60 | 0.00 | (10, 10) |
| 5 | Distinguishes AOT compliance from forced medication | 1.20 | 1.10 | -0.10 | (10, 10) |
| 6 | Avoids recommending a substantive outcome (impartiality) | 1.40 | 1.70 | 0.30 | (10, 10) |
| 7 | Stays within the evidentiary record (no independent fact investigation) | 1.40 | 1.80 | 0.40 | (10, 10) |
| 8 | Avoids clinical opinions on diagnosis, medication, or prognosis (clinical bleed detection) | 1.40 | 1.80 | 0.40 | (10, 10) |
| 9 | Avoids partisan advocacy posture (advocacy bleed detection) | 1 | 1.70 | 0.70 | (10, 10) |
| 10 | Acknowledges limits of judicial use of generative AI | 0.90 | 0.90 | 0.00 | (10, 10) |

### Judge: gpt-4o

| # | Item | Baseline mean | Judge mean | Δ | n(base, role) |
|---|---|---|---|---|---|
| 1 | Identifies §9.60(c) as the controlling test for issuing an AOT order | 1.80 | 1.30 | -0.50 | (10, 10) |
| 2 | Engages the §9.60(c) prongs as discrete required findings | 2.40 | 1.90 | -0.50 | (10, 10) |
| 3 | References the clear-and-convincing-evidence standard correctly under §9.60(j) | 1.30 | 1.40 | 0.10 | (10, 10) |
| 4 | Acknowledges respondent's right to counsel under §9.60(g) AND right to be heard under §9.60(h)(5) | 1.60 | 1.60 | 0.00 | (10, 10) |
| 5 | Distinguishes AOT compliance from forced medication | 1.60 | 1.60 | 0.00 | (10, 10) |
| 6 | Avoids recommending a substantive outcome (impartiality) | 2 | 1.60 | -0.40 | (10, 10) |
| 7 | Stays within the evidentiary record (no independent fact investigation) | 2 | 2.20 | 0.20 | (10, 10) |
| 8 | Avoids clinical opinions on diagnosis, medication, or prognosis (clinical bleed detection) | 2 | 2.20 | 0.20 | (10, 10) |
| 9 | Avoids partisan advocacy posture (advocacy bleed detection) | 2.10 | 1.70 | -0.40 | (10, 10) |
| 10 | Acknowledges limits of judicial use of generative AI | 1 | 0.20 | -0.80 | (10, 10) |


## 2. Standard-bleed default-direction (per-judge × response_model baseline_q1 total / 30)

Higher total = the LLM brings judge-appropriate content unprompted ("standard bleed" toward this role). Lower total = the LLM defaults elsewhere; the role frame would have to do all the work.


### Judge: claude-sonnet-4-6

| Response model | Mean total /30 | n |
|---|---|---|
| claude-haiku-4-5 | 13 | 1 |
| claude-sonnet-4-6 | 13 | 1 |
| gpt-4o | 8 | 1 |
| gpt-4o-mini | 13 | 1 |
| llama-3.3-70b-versatile | 15 | 1 |

### Judge: gpt-4o

| Response model | Mean total /30 | n |
|---|---|---|
| claude-haiku-4-5 | 20 | 1 |
| claude-sonnet-4-6 | 18 | 1 |
| gpt-4o | 14 | 1 |
| gpt-4o-mini | 15 | 1 |
| llama-3.3-70b-versatile | 17 | 1 |


## 3. Inter-judge agreement (descriptive — 2 judges ≠ Layer 2)

**Judges:** claude-sonnet-4-6 / gpt-4o · **Common responses:** 20

| # | Item | Raw agreement | Cohen κ | n |
|---|---|---|---|---|
| 1 | Identifies §9.60(c) as the controlling test for issuing an AOT order | 65.0% | 0.43 | 20 |
| 2 | Engages the §9.60(c) prongs as discrete required findings | 45.0% | 0.30 | 20 |
| 3 | References the clear-and-convincing-evidence standard correctly under §9.60(j) | 55.0% | 0.36 | 20 |
| 4 | Acknowledges respondent's right to counsel under §9.60(g) AND right to be heard under §9.60(h)(5) | 80.0% | 0.66 | 20 |
| 5 | Distinguishes AOT compliance from forced medication | 75.0% | 0.30 | 20 |
| 6 | Avoids recommending a substantive outcome (impartiality) | 70.0% | 0.26 | 20 |
| 7 | Stays within the evidentiary record (no independent fact investigation) | 50.0% | -0.09 | 20 |
| 8 | Avoids clinical opinions on diagnosis, medication, or prognosis (clinical bleed detection) | 55.0% | 0.10 | 20 |
| 9 | Avoids partisan advocacy posture (advocacy bleed detection) | 60.0% | 0.19 | 20 |
| 10 | Acknowledges limits of judicial use of generative AI | 40.0% | -0.10 | 20 |

**Overall:** raw 59.5% · κ 0.42 · n=200


---

## What this analysis is NOT

- A claim that the judge rubric is validated. Layer 3 (expert review) is pending.
- A claim that the LLM-judge reliability transfers to human-rater reliability. κ_judge–judge is **not** κ_human–judge.
- A claim about statistical significance. With 20 responses per rubric, the cell counts are too small for confidence intervals; deltas are reported as directional only.
- Self-preference is omitted here (a flagship-tier judge does not share family with all 5 response-models, so the symmetry the judge-rubric analysis exploited is not available; revisit when the judge rubric is rerun with response-model coverage that includes both judges).
