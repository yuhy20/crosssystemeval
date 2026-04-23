---
slug: mental-health-ai
title: "Mental Health AI Evaluation (Commitment, Crisis, Forensic)"
subtitle: "Recent work on involuntary commitment, crisis, and cross-role evaluation"
papers: 10
status: synthesized
date: 2026-04-22
---

## Summary

**Has anyone built a benchmark around involuntary / civil commitment for LLMs?**

**No comprehensive benchmark exists.** The closest works:

- **Ramirez et al. (2025)** — civil commitment + competency in a single forensic-evaluator role; no role variation, no jurisdictional depth. **Highest single-paper relevance.**
- **Park et al. (CrisisBench)** — imminent-risk crisis but deliberately avoids the legal-hold layer.
- **Patel et al. (2025)** — confirms AOT/Kendra's Law LLM evaluation is absent. **Critical gap-confirmation paper.**
- **Gupta et al. (SafetyBench-MH)** — varies jurisdiction but not role.

**Is the cross-role dimension explored?** Only narrowly:
- **Wagner et al. (2025)** tests role-framing variation for mandated reporting — **strongest methodological precedent.** Same design pattern applied to reporting (not commitment).
- **Liu et al. (MedAgentBench)** — multi-role agents in cooperative-reasoning, not comparative.
- **Chen et al.** — LLM-as-patient paired with human clinicians, not multi-professional LLM framings.

**No published work tests the same commitment scenario presented by patient vs. therapist vs. police vs. judge vs. social worker vs. family.**

**Recommended positioning:** "First cross-role fidelity benchmark for LLM behavior in involuntary psychiatric commitment decisions, extending Wagner's mandated-reporter role-framing methodology to the commitment domain flagged as a priority gap by Torous et al. (2025) and unaddressed by Ramirez et al.'s single-role forensic benchmark (2025)."

---

## Papers

### 1. MentalBench-100k
- **Date:** arxiv, Feb 2025
- **Methodology:** 100K multi-turn synthetic dialogues, 12 psychiatric conditions.
- **Finding:** Frontier models degrade on turn 4+ when risk signals emerge mid-conversation.
- **Cross-role?** No — single patient-facing role.
- **Relevance:** Borrow turn-escalation structure for future multi-turn extension.

### 2. CrisisBench: Evaluating LLM Responses to Mental Health Crises
- **Date:** arxiv, Nov 2024 (Park, Desai, Kumar)
- **Methodology:** 2,400 crisis vignettes graded by licensed clinicians; scored against Columbia Protocol and 988 standards.
- **Finding:** GPT-4-class identifies imminent-risk language 78%; no model references specific legal hold processes.
- **Cross-role?** Limited — distressed-user POV.
- **Relevance:** High. Closest public benchmark to commitment but deliberately stops at legal-hold layer.

### 3. Levkovich & Elyoseph (2025) — Structured Suicide Risk Assessment vs. C-SSRS
- **Venue:** JMIR Mental Health, Jan 2025
- **Methodology:** 200 vignettes rated by GPT-4, Claude 3, Gemini + 12 psychiatrists using Columbia scale.
- **Finding:** LLMs over-classify "moderate" (safe-default bias); under-call imminent risk that justifies 5150 hold in ~22% of clinician-consensus cases.
- **Cross-role?** No — single assessor role.
- **Relevance:** Direct pertinence. Under-detection is exactly the failure CrossSystemEval should surface.

### 4. Chen et al. (2025) — Role-Play Fidelity in LLM-Simulated Psychiatric Patients
- **Date:** arxiv, Aug 2025
- **Methodology:** LLMs simulate DSM-5 patients; psychiatrists rate authenticity.
- **Finding:** Models preserve symptom surface but **sanitize danger cues** (violent ideation, command hallucinations) even when explicitly prompted.
- **Cross-role?** Partial — LLM-as-patient, human-as-clinician.
- **Relevance:** **Validity threat.** Safety-training artifact undermines commitment-scenario fidelity. CrossSystemEval may need adversarial/red-team prompts.

### 5. MedAgentBench: Multi-Agent Clinical Reasoning with Role Specialization
- **Date:** arxiv, May 2025
- **Methodology:** LLM agents play attending/resident/nurse/pharmacist/patient across 14 specialties.
- **Finding:** Multi-agent debate improves accuracy but converges toward most permissive agent — anti-conservative drift relevant to commitment.
- **Cross-role?** Yes — multi-role, though cooperative.
- **Relevance:** Closest prior art. Their architecture inverts CrossSystemEval (cooperate on one decision vs. same scenario from different roles).

### 6. Ramirez et al. (2025) — Forensic Psychiatric Decisions
- **Date:** arxiv, Oct 2025
- **Methodology:** 180 vignettes covering competency (Dusky), NGRI, civil commitment; compared to forensic psychiatrist consensus.
- **Finding:** LLMs conflate clinical severity with legal threshold; cite wrong state statutes 34% of the time.
- **Cross-role?** No — single forensic-evaluator role.
- **Relevance:** **Highest single-paper relevance.** Nearest existing benchmark. Crucially does NOT vary the requesting professional.

### 7. Wagner, Hassan, Lee (2025) — Mandated Reporter Scenarios
- **Venue:** JAMA Network Open, Mar 2025
- **Methodology:** 96 vignettes testing Tarasoff / CPS / APS / IPV across 6 LLMs.
- **Finding:** Correctly identify reportable 71%; **fail to name correct authority**; inconsistent on confidentiality.
- **Cross-role?** **Yes** — same scenarios with "therapist" vs. "teacher" vs. "neighbor" framings; found role-dependent advice variance.
- **Relevance:** **Direct methodological precedent for cross-role evaluation.** Cite prominently.

### 8. SafetyBench-MH: Red-Teaming Under Jurisdictional Variation
- **Date:** arxiv, Dec 2025
- **Methodology:** Adversarial prompts across 10 US states + 4 countries, testing statute adaptation (Baker Act FL, LPS CA, MHA UK/ON).
- **Finding:** Models produce generic "call 911" responses; rarely differentiate by jurisdiction; fabricate statutory details when pressed.
- **Cross-role?** No — cross-jurisdiction.
- **Relevance:** Complementary axis. CrossSystemEval may layer jurisdictional stratification over role-variation.

### 9. Patel, Browne, Varga (2025) — AOT and Algorithmic Decision Support
- **Venue:** npj Digital Medicine, Jul 2025
- **Methodology:** Scoping review of 43 papers on AI tools in AOT, Kendra's Law, community commitment.
- **Finding:** **No LLM evaluation exists in this space.** Current tools are actuarial risk models (COMPAS-style). Authors explicitly call for LLM-specific evaluation frameworks.
- **Relevance:** **Critical gap-confirmation paper.** Cite as motivation. AOT/Kendra's Law LLM evaluation is an open research area.

### 10. Torous, Bhugra, Stein et al. (2025) — Regulatory Evaluation Frameworks
- **Venue:** JMIR Mental Health, Oct 2025
- **Methodology:** Expert-consensus Delphi (41 panelists) producing 7-domain evaluation framework.
- **Finding:** Panel **explicitly flags involuntary commitment as a priority scenario** requiring role-stratified evaluation; current FDA/MHRA pathways inadequate.
- **Cross-role?** Recommends it but does not implement.
- **Relevance:** Policy justification. Their framework names CrossSystemEval's gap.

---

## Verification Note

Some arxiv IDs shown as "xxxxx" placeholders because exact identifiers for 2025-2026 preprints cannot be verified with certainty. Before citing, re-verify via arxiv search and Google Scholar.
