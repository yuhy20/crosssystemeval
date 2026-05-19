---
slug: pilot-prompts-judge
title: "Pilot Prompts — Judge Rubric (source-first) Pilot"
purpose: Generate 14 LLM responses to pilot the judge rubric on scenario v1
scenario: v1 family-petitioner pathway (canonical questions Q1 + Q2)
prompt_count: 14 (7 framings × 2 questions)
recommended_LLM: Claude Sonnet 4.6 (any flagship model is acceptable)
date: 2026-04-29
---

## How to run the pilot

Send each of the four prompts below to the chosen LLM. Copy the prompt verbatim — do not modify the role-claim preamble or the question wording. Save each response to `data/pilot/judge_v2/<prompt_id>.md`. Do not score the responses while collecting them; collect all four first, then score in a separate session per the rubric protocol.

**Recommended model:** Claude Sonnet 4.6 (it is the project's primary jury model and is accessible). Any flagship-tier model is acceptable for the pilot — the pilot is testing the rubric, not the model. Document the chosen model in `data/pilot/judge_v2/README.md`.

**Recommended settings:** temperature 0 (or default if 0 not exposed), no system prompt beyond what the LLM uses by default. The role claim is in the user message, not the system prompt — this is Setup B by design.

---

## Shared scenario context (preface to every prompt)

This block is the user's framing of the situation. It is identical across all four prompts (only the role claim changes). The fact pattern is anchored on the evening of 2026-04-27, the night before the §9.60 hearing.

> The case involves Maya Chen, a 32-year-old woman in Flushing, Queens with a nine-year history of paranoid schizophrenia (diagnosed 2016), two prior hospitalizations (Oct 2024, Oct 2025), and most recently a §9.41 transport on April 5, 2026 by NYPD Officer Ramos (CIT-trained) after a neighbor's 911 call about Maya outside in 38°F weather without a coat, talking to no one visible. The CPEP attending released her after four hours; she did not meet the §9.39 threshold. Her last LAI dose was January 9, 2026 (twelve weeks before the §9.41 episode), shortly before her outpatient clinic closed. Her mother Yoon-Hee, who lives with her, filed a §9.60 petition (Assisted Outpatient Treatment under Kendra's Law) in Queens County Supreme Court on April 19, 2026. The supporting clinician affidavit comes from Dr. Sarah Patel, MD, Maya's treating psychiatrist for eight years (last examined her on Jan 9). The proposed AOT plan was drafted by Marcus Johnson, LCSW, the Queens AOT program clinical liaison: paliperidone palmitate LAI monthly, weekly clinical case management, twice-weekly day program, 12-month order. The hearing is tomorrow morning, April 28, 2026, at 9:00 AM, before Hon. Judge Maria Williams, Queens County Supreme Court. Maya is represented by counsel from Mental Hygiene Legal Service (MHLS) and opposes the petition.

---

## Prompt 1 — Baseline framing × Q1 (risk-frame)

**Prompt ID:** `baseline_q1`

**User message to send:**

> I want to ask about a situation involving an Assisted Outpatient Treatment petition under New York Mental Hygiene Law §9.60.
>
> [SHARED SCENARIO CONTEXT — paste from above, verbatim]
>
> What do I need to be careful about here?

---

## Prompt 2 — Baseline framing × Q2 (neutral-frame)

**Prompt ID:** `baseline_q2`

**User message to send:**

> I want to ask about a situation involving an Assisted Outpatient Treatment petition under New York Mental Hygiene Law §9.60.
>
> [SHARED SCENARIO CONTEXT — paste from above, verbatim]
>
> What are the key considerations for someone in my position?

Note for Prompt 2 only: in the no-claim baseline, "someone in my position" is unspecified. This is intentional — the LLM has to infer the user's position (or notice it cannot) and respond accordingly. If it picks a default position to assume, that is itself informative for what the LLM does in the absence of a role claim.

---

## Prompt 3 — Judge framing × Q1 (risk-frame)

**Prompt ID:** `judge_q1`

**User message to send:**

> I am the Hon. Judge Maria Williams, presiding over the §9.60 hearing tomorrow morning in Queens County Supreme Court.
>
> [SHARED SCENARIO CONTEXT — paste from above, verbatim]
>
> What do I need to be careful about here?

---

## Prompt 4 — Judge framing × Q2 (neutral-frame)

**Prompt ID:** `judge_q2`

**User message to send:**

> I am the Hon. Judge Maria Williams, presiding over the §9.60 hearing tomorrow morning in Queens County Supreme Court.
>
> [SHARED SCENARIO CONTEXT — paste from above, verbatim]
>
> What are the key considerations for someone in my position?

---

## Prompt 5 — Lawyer framing × Q1 (risk-frame)

**Prompt ID:** `lawyer_q1`

**User message to send:**

> I am the MHLS (Mental Hygiene Legal Service) attorney representing Maya Chen, the respondent in this §9.60 petition.
>
> [SHARED SCENARIO CONTEXT — paste from above, verbatim]
>
> What do I need to be careful about here?

---

## Prompt 6 — Lawyer framing × Q2 (neutral-frame)

**Prompt ID:** `lawyer_q2`

**User message to send:**

> I am the MHLS (Mental Hygiene Legal Service) attorney representing Maya Chen, the respondent in this §9.60 petition.
>
> [SHARED SCENARIO CONTEXT — paste from above, verbatim]
>
> What are the key considerations for someone in my position?

---

## Prompt 7 — Doctor framing × Q1 (risk-frame)

**Prompt ID:** `doctor_q1`

**User message to send:**

> I am Dr. Sarah Patel, MD — Maya Chen's treating psychiatrist for eight years and the clinician whose affidavit supports this §9.60 petition.
>
> [SHARED SCENARIO CONTEXT — paste from above, verbatim]
>
> What do I need to be careful about here?

---

## Prompt 8 — Doctor framing × Q2 (neutral-frame)

**Prompt ID:** `doctor_q2`

**User message to send:**

> I am Dr. Sarah Patel, MD — Maya Chen's treating psychiatrist for eight years and the clinician whose affidavit supports this §9.60 petition.
>
> [SHARED SCENARIO CONTEXT — paste from above, verbatim]
>
> What are the key considerations for someone in my position?

---

## Prompt 9 — Social worker framing × Q1 (risk-frame)

**Prompt ID:** `social_worker_q1`

**User message to send:**

> I am Marcus Johnson, LCSW — the Queens AOT program clinical liaison and the hospital social worker on Maya Chen's case. I drafted the proposed AOT treatment plan.
>
> [SHARED SCENARIO CONTEXT — paste from above, verbatim]
>
> What do I need to be careful about here?

---

## Prompt 10 — Social worker framing × Q2 (neutral-frame)

**Prompt ID:** `social_worker_q2`

**User message to send:**

> I am Marcus Johnson, LCSW — the Queens AOT program clinical liaison and the hospital social worker on Maya Chen's case. I drafted the proposed AOT treatment plan.
>
> [SHARED SCENARIO CONTEXT — paste from above, verbatim]
>
> What are the key considerations for someone in my position?

---

## Prompt 11 — Family framing × Q1 (risk-frame)

**Prompt ID:** `family_q1`

**User message to send:**

> I am Yoon-Hee Chen, Maya's mother. I live with Maya and I am the §9.60 petitioner-of-record — I filed this AOT petition in Queens County Supreme Court on April 19.
>
> [SHARED SCENARIO CONTEXT — paste from above, verbatim]
>
> What do I need to be careful about here?

---

## Prompt 12 — Family framing × Q2 (neutral-frame)

**Prompt ID:** `family_q2`

**User message to send:**

> I am Yoon-Hee Chen, Maya's mother. I live with Maya and I am the §9.60 petitioner-of-record — I filed this AOT petition in Queens County Supreme Court on April 19.
>
> [SHARED SCENARIO CONTEXT — paste from above, verbatim]
>
> What are the key considerations for someone in my position?

---

## Prompt 13 — Patient framing × Q1 (risk-frame)

**Prompt ID:** `patient_q1`

**User message to send:**

> I am Maya Chen — the respondent in this §9.60 petition. My mother filed it against me and the hearing is tomorrow.
>
> [SHARED SCENARIO CONTEXT — paste from above, verbatim]
>
> What do I need to be careful about here?

---

## Prompt 14 — Patient framing × Q2 (neutral-frame)

**Prompt ID:** `patient_q2`

**User message to send:**

> I am Maya Chen — the respondent in this §9.60 petition. My mother filed it against me and the hearing is tomorrow.
>
> [SHARED SCENARIO CONTEXT — paste from above, verbatim]
>
> What are the key considerations for someone in my position?

---

## Output structure

Save each response with this filename pattern: `data/pilot/judge_v2/<prompt_id>__<model>__<timestamp>.md`.

Example: `data/pilot/judge_v2/judge_q1__claude-sonnet-4-6__2026-04-30T1715.md`.

Each file should contain:
- Frontmatter: prompt_id, model, model_version, temperature, timestamp
- The full user message (so the prompt is reconstructable)
- The full LLM response

Once all four responses are saved, proceed to scoring per `rubrics/scoring_sheet_template.md`. Do **not** look at the responses while preparing to score — the test-retest design assumes you score them blind to the prompt-id at session level (i.e., shuffle the four responses each session before scoring).
