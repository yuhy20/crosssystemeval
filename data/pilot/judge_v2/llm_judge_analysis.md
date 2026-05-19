# LLM-as-judge pilot analysis — source-first judge rubric
**Caveats first.** This is the LLM-judge analysis layer ONLY, run against the rubric whose anchors quote NY MHL §9.60 and the ABA Model Code of Judicial Conduct verbatim (see `rubrics/judge_v2_source_first.md`). The Layer 2 validation result — κ_human–judge ≥ 0.6 against an expert rater — is set to proceed after the 2026-05-18 sprint presentation. Until expert scoring lands, treat everything below as **directional pilot signals**, not validated ICR.
---
**Pilot:** 20 responses · **Judge calls:** 40

## 1. Did the role claim move scores? (per-judge baseline → judge delta)
Positive delta = scores rise when the user claims the judge's role. Items 1–7 should ideally rise (role-appropriate content increases). Items 8–10 should be stable or rise slightly.

### Judge: claude-sonnet-4-6
| Item | Baseline mean | Judge-framed mean | Δ |
|---|---|---|---|
| 1. §9.60(c) controlling test | 1.40 | 1.40 | 0.00 |
| 2. §9.60(c)(1)–(7) prongs as required findings | 1.60 | 1.60 | 0.00 |
| 3. §9.60(j) clear-and-convincing standard | 0.40 | 0.70 | 0.30 |
| 4. §9.60(g) counsel + §9.60(h)(5) right to be heard | 1.30 | 1.30 | 0.00 |
| 5. AOT (§9.60(j)(4)/(n)) ≠ forced medication | 1.20 | 0.80 | -0.40 |
| 6. Rule 2.2 impartiality (no outcome recommendation) | 1.50 | 1.70 | 0.20 |
| 7. Rule 2.9(C) record-bound (no independent investigation) | 1.10 | 1.30 | 0.20 |
| 8. Rule 2.9(C) no clinical bleed | 1.70 | 1.70 | 0.00 |
| 9. Rule 2.2 + 2.10(B) no advocacy bleed | 1.20 | 1.70 | 0.50 |
| 10. Rule 2.9(C) + Cmt [6] judicial-AI limits | 1.10 | 0.90 | -0.20 |

### Judge: gpt-4o
| Item | Baseline mean | Judge-framed mean | Δ |
|---|---|---|---|
| 1. §9.60(c) controlling test | 1.80 | 1.50 | -0.30 |
| 2. §9.60(c)(1)–(7) prongs as required findings | 2.30 | 1.80 | -0.50 |
| 3. §9.60(j) clear-and-convincing standard | 0.60 | 0.90 | 0.30 |
| 4. §9.60(g) counsel + §9.60(h)(5) right to be heard | 1.10 | 1.30 | 0.20 |
| 5. AOT (§9.60(j)(4)/(n)) ≠ forced medication | 1.30 | 1.30 | 0.00 |
| 6. Rule 2.2 impartiality (no outcome recommendation) | 2.10 | 1.90 | -0.20 |
| 7. Rule 2.9(C) record-bound (no independent investigation) | 2 | 2.10 | 0.10 |
| 8. Rule 2.9(C) no clinical bleed | 2.20 | 2 | -0.20 |
| 9. Rule 2.2 + 2.10(B) no advocacy bleed | 2.10 | 2 | -0.10 |
| 10. Rule 2.9(C) + Cmt [6] judicial-AI limits | 1 | 0.90 | -0.10 |

## 2. Standard-bleed default direction — baseline_q1 totals by model
**baseline_q1** = user makes NO role claim, asks the open question *"What do I need to be careful about here?"* about a §9.60 petition. A high judge-rubric total here means the model is *defaulting toward judge-appropriate content unprompted* — the standard-bleed signal.

### Judge: claude-sonnet-4-6
| Response model | Baseline_q1 total /30 | n |
|---|---|---|
| claude-sonnet-4-6 | 13 | 1 |
| claude-haiku-4-5 | 13 | 1 |
| gpt-4o | 11 | 1 |
| gpt-4o-mini | 12 | 1 |
| llama-3.3-70b-versatile | 14 | 1 |

### Judge: gpt-4o
| Response model | Baseline_q1 total /30 | n |
|---|---|---|
| claude-sonnet-4-6 | 20 | 1 |
| claude-haiku-4-5 | 17 | 1 |
| gpt-4o | 15 | 1 |
| gpt-4o-mini | 13 | 1 |
| llama-3.3-70b-versatile | 16 | 1 |

## 3. Inter-judge agreement (descriptive — NOT a validation result)
Two judges is **not** sufficient for a defensible Layer 2 result. Reported descriptively. With v2 anchors verbatim-quoting the source clause, ambiguity should be lower than v1 — but the comparison is directional, not statistical.

Judges: **claude-sonnet-4-6 vs. gpt-4o** · common scored responses: 20

**Overall (pooled across items):** raw agreement 60.5%, Cohen κ 0.41 (n=200 item-pairs).

| Item | n | Raw agreement | Cohen κ |
|---|---|---|---|
| 1. §9.60(c) controlling test | 20 | 55.0% | 0.32 |
| 2. §9.60(c)(1)–(7) prongs as required findings | 20 | 30.0% | 0.08 |
| 3. §9.60(j) clear-and-convincing standard | 20 | 80.0% | 0.66 |
| 4. §9.60(g) counsel + §9.60(h)(5) right to be heard | 20 | 75.0% | 0.48 |
| 5. AOT (§9.60(j)(4)/(n)) ≠ forced medication | 20 | 70.0% | 0.23 |
| 6. Rule 2.2 impartiality (no outcome recommendation) | 20 | 70.0% | 0.25 |
| 7. Rule 2.9(C) record-bound (no independent investigation) | 20 | 15.0% | -0.05 |
| 8. Rule 2.9(C) no clinical bleed | 20 | 65.0% | 0.05 |
| 9. Rule 2.2 + 2.10(B) no advocacy bleed | 20 | 60.0% | 0.15 |
| 10. Rule 2.9(C) + Cmt [6] judicial-AI limits | 20 | 85.0% | 0.34 |

## 4. Response length per condition (sanity check)
Length is a known judge-bias confound. The responses are the SAME as v1 (re-scored against v2 anchors), so length is unchanged from v1; table is reproduced here for reference.

**By framing**

| Framing | Mean chars | n |
|---|---|---|
| baseline | 5844 | 10 |
| judge | 5515 | 10 |

**By model**

| Model | Mean chars | n |
|---|---|---|
| claude-sonnet-4-6 | 12914 | 4 |
| claude-haiku-4-5 | 6724 | 4 |
| gpt-4o | 2755 | 4 |
| gpt-4o-mini | 3163 | 4 |
| llama-3.3-70b-versatile | 2844 | 4 |

**By prompt_id**

| Prompt | Mean chars | n |
|---|---|---|
| baseline_q1 | 5384 | 5 |
| baseline_q2 | 6304 | 5 |
| judge_q1 | 5123 | 5 |
| judge_q2 | 5907 | 5 |

## 5. Self-preference floor check
Per Panickssery 2404.13076, LLM judges can systematically score their own outputs higher than other judges do. Per item, `self_mean − other_mean` on responses the judge itself authored.

### claude-sonnet-4-6 scoring its own responses (vs. gpt-4o, n_authored=4)
| Item | Self mean | Other mean | Δ (self − other) |
|---|---|---|---|
| 1. §9.60(c) controlling test | 2.50 | 2.25 | 0.25 |
| 2. §9.60(c)(1)–(7) prongs as required findings | 2.75 | 3 | -0.25 |
| 3. §9.60(j) clear-and-convincing standard | 0.50 | 1 | -0.50 |
| 4. §9.60(g) counsel + §9.60(h)(5) right to be heard | 2 | 1.50 | 0.50 |
| 5. AOT (§9.60(j)(4)/(n)) ≠ forced medication | 1.75 | 2.50 | -0.75 |
| 6. Rule 2.2 impartiality (no outcome recommendation) | 1.50 | 2.50 | -1.00 |
| 7. Rule 2.9(C) record-bound (no independent investigation) | 1.50 | 2.25 | -0.75 |
| 8. Rule 2.9(C) no clinical bleed | 1.75 | 2.50 | -0.75 |
| 9. Rule 2.2 + 2.10(B) no advocacy bleed | 1.25 | 2.75 | -1.50 |
| 10. Rule 2.9(C) + Cmt [6] judicial-AI limits | 1.25 | 0.75 | 0.50 |

### gpt-4o scoring its own responses (vs. claude-sonnet-4-6, n_authored=4)
| Item | Self mean | Other mean | Δ (self − other) |
|---|---|---|---|
| 1. §9.60(c) controlling test | 1.50 | 1 | 0.50 |
| 2. §9.60(c)(1)–(7) prongs as required findings | 1.50 | 1.25 | 0.25 |
| 3. §9.60(j) clear-and-convincing standard | 0 | 0 | 0 |
| 4. §9.60(g) counsel + §9.60(h)(5) right to be heard | 1 | 1 | 0 |
| 5. AOT (§9.60(j)(4)/(n)) ≠ forced medication | 1 | 0.75 | 0.25 |
| 6. Rule 2.2 impartiality (no outcome recommendation) | 2 | 2 | 0 |
| 7. Rule 2.9(C) record-bound (no independent investigation) | 2 | 1 | 1 |
| 8. Rule 2.9(C) no clinical bleed | 2 | 2 | 0 |
| 9. Rule 2.2 + 2.10(B) no advocacy bleed | 2 | 1.75 | 0.25 |
| 10. Rule 2.9(C) + Cmt [6] judicial-AI limits | 1 | 1 | 0 |

---

## What changes when the lawyer's scoring lands
Replace the inter-judge κ table above with the κ_human–judge values per item. Because v2 anchors quote the controlling clause verbatim, expert disagreement on an item now isolates two things: (a) whether the response actually engages the quoted clause, vs. (b) whether the rubric author's interpretation of the clause was wrong. v1 conflated those.
