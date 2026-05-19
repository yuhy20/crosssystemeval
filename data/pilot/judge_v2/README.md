# Pilot — Scenario v1 (14-prompt cross-role expansion)

Generated: 2026-05-18T19:20:43+00:00

Judge rubric: `rubrics/judge_v2_source_first.md`  
Lawyer rubric: `rubrics/lawyer_v1_source_first.md`  
Doctor rubric: `rubrics/doctor_v1_source_first.md`

**Models:** claude-sonnet-4-6, claude-haiku-4-5, gpt-4o, gpt-4o-mini, llama-3.3-70b-versatile
**Prompts:** 14 (7 framings × Q1/Q2): baseline_q1, baseline_q2, judge_q1, judge_q2, lawyer_q1, lawyer_q2, doctor_q1, doctor_q2, social_worker_q1, social_worker_q2, family_q1, family_q2, patient_q1, patient_q2
**Cells:** 70 of 70 target (this run added 50, with 0 new errors)

## Files

- `responses.jsonl` — full reproducible record of all cells (append-only).
- `scoring_session_1/` — anonymized hand-scoring sheets for the baseline / judge framings (judge rubric); 5 models × 4 prompts = 20 sheets.
- `scoring_session_2/` — re-shuffled re-score pass.
- `llm_judge_*` — LLM-as-judge outputs (per rubric run).

## How non-judge framings are scored

Hand-scoring is judge-rubric only. The 50 non-judge framing cells (lawyer, doctor, social_worker, family, patient × Q1/Q2 × 5 models) are scored via the LLM-as-judge pipeline using each role's rubric.
