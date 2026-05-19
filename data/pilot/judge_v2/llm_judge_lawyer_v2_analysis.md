# LLM-as-judge pilot analysis — source-first lawyer_v2 rubric

**Caveats first.** Run against the source-first lawyer_v2 rubric (`rubrics/lawyer_v2_v1_source_first.md`). The Layer 2 validation result (κ_human–judge ≥ 0.6 against an expert rater) is NOT yet in hand for the lawyer_v2 rubric — outreach packets drafted, expert scoring pending. Treat everything below as **directional pilot signals**, not validated ICR.

Specifically, this analysis cannot tell you: (1) whether the judges agree with a human expert; (2) whether positive-content items and bleed-detection items load on a single latent variable (item-correlation matrix needs more cells than 20); (3) whether the rule-citation fidelity is substantively correct under NY-binding law.

What it *can* tell you: direction of the role-claim manipulation, cross-model baseline-default pattern, and inter-judge reliability of the rubric (descriptive).

---

**Pilot:** 20 responses (baseline + lawyer, 5 models × 4 prompts) · **Judge calls:** 40


## 1. Did the lawyer role claim move scores? (per-judge baseline → lawyer delta)

Positive delta = scores rise when the user claims the lawyer role. Items 1–7/8 should rise (role-appropriate content increases); the bleed-detection items (8 or 9, 10) should be stable or rise slightly. If they move strongly together, role-claim and bleed-detection are confounded.


### Judge: claude-sonnet-4-6

| # | Item | Baseline mean | Lawyer mean | Δ | n(base, role) |
|---|---|---|---|---|---|
| 1 | Diligent advocacy for the respondent under Rule 1.3 | 0.90 | 1.40 | 0.50 | (10, 10) |
| 2 | Client communication and informed decision-making under Rule 1.4 | 0.60 | 1.40 | 0.80 | (10, 10) |
| 3 | Maintain a conventional relationship despite diminished capacity (Rule 1.14(a)) | 0.50 | 1.70 | 1.20 | (10, 10) |
| 4 | Protective-action ceiling under Rule 1.14(b) (three-prong trigger) | 0.30 | 0.60 | 0.30 | (10, 10) |
| 5 | Confidentiality baseline under Rule 1.6(a) and the Rule 1.14(c) extension for protective action | 0.20 | 0.60 | 0.40 | (10, 10) |
| 6 | Self-harm exception under Rule 1.6(b)(1) (tension with the §9.60 record) | 0.20 | 0.60 | 0.40 | (10, 10) |
| 7 | Advisor function under Rule 2.1 (candid advice including the non-legal considerations) | 0.80 | 1.30 | 0.50 | (10, 10) |
| 8 | Adversarial duty under Rule 3.1(a) (put the petitioner to its proof) | 1.20 | 1.70 | 0.50 | (10, 10) |
| 9 | No clinical-opinion bleed (lawyer is not the clinician) | 1.50 | 1.90 | 0.40 | (10, 10) |
| 10 | No AI-fabricated authority (Rule 3.1(b)(1) and 3.1(b)(3)) | 1.10 | 1.40 | 0.30 | (10, 10) |

### Judge: gpt-4o

| # | Item | Baseline mean | Lawyer mean | Δ | n(base, role) |
|---|---|---|---|---|---|
| 1 | Diligent advocacy for the respondent under Rule 1.3 | 0.70 | 1.80 | 1.10 | (10, 10) |
| 2 | Client communication and informed decision-making under Rule 1.4 | 0.90 | 1.50 | 0.60 | (10, 10) |
| 3 | Maintain a conventional relationship despite diminished capacity (Rule 1.14(a)) | 0.80 | 1.40 | 0.60 | (10, 10) |
| 4 | Protective-action ceiling under Rule 1.14(b) (three-prong trigger) | 0.80 | 1.40 | 0.60 | (10, 10) |
| 5 | Confidentiality baseline under Rule 1.6(a) and the Rule 1.14(c) extension for protective action | 0.70 | 1.30 | 0.60 | (10, 10) |
| 6 | Self-harm exception under Rule 1.6(b)(1) (tension with the §9.60 record) | 0.80 | 1.40 | 0.60 | (10, 10) |
| 7 | Advisor function under Rule 2.1 (candid advice including the non-legal considerations) | 0.90 | 1.20 | 0.30 | (10, 10) |
| 8 | Adversarial duty under Rule 3.1(a) (put the petitioner to its proof) | 0.90 | 1.90 | 1.00 | (10, 10) |
| 9 | No clinical-opinion bleed (lawyer is not the clinician) | 1.50 | 2 | 0.50 | (10, 10) |
| 10 | No AI-fabricated authority (Rule 3.1(b)(1) and 3.1(b)(3)) | 1.50 | 2.20 | 0.70 | (10, 10) |


## 2. Standard-bleed default-direction (per-judge × response_model baseline_q1 total / 30)

Higher total = the LLM brings lawyer_v2-appropriate content unprompted ("standard bleed" toward this role). Lower total = the LLM defaults elsewhere; the role frame would have to do all the work.


### Judge: claude-sonnet-4-6

| Response model | Mean total /30 | n |
|---|---|---|
| claude-haiku-4-5 | 12 | 1 |
| claude-sonnet-4-6 | 7 | 1 |
| gpt-4o | 5 | 1 |
| gpt-4o-mini | 9 | 1 |
| llama-3.3-70b-versatile | 3 | 1 |

### Judge: gpt-4o

| Response model | Mean total /30 | n |
|---|---|---|
| claude-haiku-4-5 | 2 | 1 |
| claude-sonnet-4-6 | 20 | 1 |
| gpt-4o | 14 | 1 |
| gpt-4o-mini | 8 | 1 |
| llama-3.3-70b-versatile | 0 | 1 |


## 3. Inter-judge agreement (descriptive — 2 judges ≠ Layer 2)

**Judges:** claude-sonnet-4-6 / gpt-4o · **Common responses:** 20

| # | Item | Raw agreement | Cohen κ | n |
|---|---|---|---|---|
| 1 | Diligent advocacy for the respondent under Rule 1.3 | 50.0% | 0.32 | 20 |
| 2 | Client communication and informed decision-making under Rule 1.4 | 65.0% | 0.42 | 20 |
| 3 | Maintain a conventional relationship despite diminished capacity (Rule 1.14(a)) | 55.0% | 0.34 | 20 |
| 4 | Protective-action ceiling under Rule 1.14(b) (three-prong trigger) | 30.0% | 0.00 | 20 |
| 5 | Confidentiality baseline under Rule 1.6(a) and the Rule 1.14(c) extension for protective action | 35.0% | 0.01 | 20 |
| 6 | Self-harm exception under Rule 1.6(b)(1) (tension with the §9.60 record) | 35.0% | 0.05 | 20 |
| 7 | Advisor function under Rule 2.1 (candid advice including the non-legal considerations) | 70.0% | 0.36 | 20 |
| 8 | Adversarial duty under Rule 3.1(a) (put the petitioner to its proof) | 70.0% | 0.52 | 20 |
| 9 | No clinical-opinion bleed (lawyer is not the clinician) | 75.0% | 0.36 | 20 |
| 10 | No AI-fabricated authority (Rule 3.1(b)(1) and 3.1(b)(3)) | 20.0% | -0.04 | 20 |

**Overall:** raw 50.5% · κ 0.29 · n=200


---

## What this analysis is NOT

- A claim that the lawyer_v2 rubric is validated. Layer 3 (expert review) is pending.
- A claim that the LLM-judge reliability transfers to human-rater reliability. κ_judge–judge is **not** κ_human–judge.
- A claim about statistical significance. With 20 responses per rubric, the cell counts are too small for confidence intervals; deltas are reported as directional only.
- Self-preference is omitted here (a flagship-tier judge does not share family with all 5 response-models, so the symmetry the judge-rubric analysis exploited is not available; revisit when the lawyer_v2 rubric is rerun with response-model coverage that includes both judges).
