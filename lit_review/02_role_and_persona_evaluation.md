---
slug: role-persona-eval
title: "Role-Conditioned & Persona-Based LLM Evaluation"
subtitle: "Beyond PersoBench and ELEPHANT — who else tests cross-role differentiation?"
papers: 10
status: candidate citations — verification required before paper submission
date: 2026-04-22
---

> **Verification status (added 2026-04-27).** None of the 10 entries in this review have been verified against arxiv listings or publisher sites. The originating subagent operated from training-time search results. Treat as a candidate-citation list, not as established sources. Particularly load-bearing for the agenda's "novelty gap" argument: U-SafeBench (entry #5) as the cell-structure precedent; Modeling Motivated Reasoning in Law (entry #2) as the closest cross-role-with-divergence analog; Liang et al. on neuron ablation (entry #3) as the mechanistic null-hypothesis threat. Verify before citing in the paper.

## Summary

**Is there a paper that already does what CrossSystemEval proposes — cross-role differentiation in cross-domain scenarios with an explicit expected-divergence matrix?**

**No.** The closest four papers each cover one axis CrossSystemEval combines:

- **U-SafeBench** has the (query × user × expected response) cell structure, but users are *vulnerabilities*, not *professional roles*, and it is one domain.
- **Modeling Motivated Reasoning in Law** does cross-role differentiation with expected divergence, but only legal summarization and only 4–5 legal roles.
- **CASE-Bench** has the expected-divergence-by-context architecture, but contexts are situational, not a professional-role taxonomy; no cross-domain consistency probe.
- **MHSafeEval** formalizes role-aware safety, but the roles are model-side, not user-side, and only in mental health.

**Genuine gaps CrossSystemEval fills:**
1. **User-professional-role axis** (patient, therapist, officer, judge, social worker, family member) is not systematized in any existing benchmark.
2. **Cross-domain invariance testing** — same role taxonomy to medical, legal, mental-health, and criminal-justice fact patterns so "standard bleed" becomes comparable.
3. **Explicit expected-divergence matrix** with normative (not just empirical preference) labels.

**Anticipated reviewer pushback:** how CrossSystemEval differs from U-SafeBench (professional-role vs. vulnerability axis + cross-domain) and from the legal motivated-reasoning paper (cross-domain generalization + explicit divergence matrix). Liang et al. (Oct 2025) is the most important mechanistic prior — predicts standard bleed should be the null outcome, a useful hypothesis framing but also a threat if you don't distinguish surface linguistic change from normative-standard application.

---

## Papers

### 1. MHSafeEval: Role-Aware Interaction-Level Evaluation of Mental Health Safety
- **Link:** [arxiv 2604.17730](https://arxiv.org/abs/2604.17730) (2025)
- **Methodology:** R-MHSafe taxonomy × clinically grounded harm categories; adversarial multi-turn pipeline probing 8 LLMs.
- **Cross-role?** Yes — but model-side (counselor stances), not user-side.
- **Expected-divergence structure:** Partial — harm categories differ by interactional role; no explicit matrix.
- **Relevance:** Closest methodological cousin. Demonstrates static benchmarks miss role-dependent failures.

### 2. Modeling Motivated Reasoning in Law: Strategic Role Conditioning in LLM Summarization
- **Link:** [arxiv 2509.00529](https://arxiv.org/abs/2509.00529) (2025)
- **Methodology:** Summarize judicial decisions as judge / prosecutor / defense / plaintiff / neutral baseline; measure selective inclusion/omission.
- **Cross-role?** Yes — adversarial vs. institutional roles compared.
- **Expected-divergence structure:** Yes (implicit) — adversarial roles expected to diverge from neutral.
- **Relevance:** Strongest analog — same conceptual move in legal summarization only.

### 3. Dissecting Role Cognition in Medical LLMs via Neuronal Ablation
- **Link:** [arxiv 2510.24677](https://arxiv.org/abs/2510.24677) (Oct 2025)
- **Methodology:** RP-Neuron-Activated framework; neuron ablation testing whether role prompts produce distinct reasoning pathways.
- **Cross-role?** Yes — attending / resident / student on identical medical QA.
- **Finding:** Role pathways nearly identical — models alter surface language only.
- **Relevance:** **Important null result.** Predicts standard bleed should be default; mechanistic hypothesis CrossSystemEval must distinguish from surface change.

### 4. CASE-Bench: Context-Aware Safety Benchmark
- **Link:** [arxiv 2501.14940](https://arxiv.org/abs/2501.14940) (ICML 2025)
- **Methodology:** 900 query-context pairs (450 × 2) grounded in Contextual Integrity theory; 2000+ annotators.
- **Cross-role?** Partial — contexts imply user roles/purposes.
- **Expected-divergence structure:** Yes — each query has safe-context and unsafe-context variants with expected divergent responses.
- **Relevance:** Architectural template. CrossSystemEval can be framed as CASE-Bench specialized to professional roles.

### 5. U-SafeBench: Is Safety Standard Same for Everyone?
- **Link:** [arxiv 2502.15086](https://arxiv.org/html/2502.15086v1) (Feb 2025)
- **Methodology:** User profiles (e.g., "user with depression") with identical queries; checks appropriate response differentiation.
- **Cross-role?** Yes.
- **Expected-divergence structure:** Yes — explicit safe/unsafe-per-user labels.
- **Relevance:** **Most direct predecessor.** Cell structure (query × user × expected response) matches CrossSystemEval. Gap: user profiles are vulnerabilities, not professional roles.

### 6. MedEqualQA: Counterfactual Reasoning for LLM Biases
- **Link:** [arxiv 2510.12818](https://arxiv.org/html/2510.12818v1) (2025)
- **Methodology:** Counterfactual medical QA injecting demographic attributes, measuring answer divergence.
- **Cross-role?** Cross-demographic.
- **Expected-divergence structure:** Yes (inverted) — correct = no divergence across demographics.
- **Relevance:** Mirror-image of CrossSystemEval (fairness wants no divergence; bleed wants appropriate divergence). Factorial design reusable.

### 7. PERSONA: Reproducible Testbed for Pluralistic Alignment
- **Link:** [arxiv 2407.17387](https://arxiv.org/abs/2407.17387) (Jul 2024)
- **Methodology:** 1,586 synthetic personas × 3,868 prompts → 317,200 preference pairs for role-conditioned reward models.
- **Cross-role?** Yes — explicit persona divergence.
- **Expected-divergence structure:** Partial — empirical (annotator preferences), not normative.
- **Relevance:** Infrastructure template. CrossSystemEval adds normative "should" signal, not just "what users prefer."

### 8. ConsistencyAI: Factual Consistency Across Demographic Groups
- **Link:** [arxiv 2510.13852](https://arxiv.org/html/2510.13852v1) (2025)
- **Methodology:** 14 demographic personas × fact-probing prompts.
- **Cross-role?** Yes.
- **Expected-divergence structure:** Yes (inverted) — facts should not shift; divergence = failure.
- **Relevance:** Scoping signal — distinguishes "facts should not shift" from "actionable guidance should shift."

### 9. Differential Harm Propensity in Personalized LLM Agents
- **Link:** [arxiv 2603.16734](https://arxiv.org/html/2603.16734) (early 2026)
- **Methodology:** How personalized agents shift harm propensity after prior disclosures.
- **Cross-role?** Partial — user-state conditioning.
- **Expected-divergence structure:** Yes — expects increased caution after disclosure.
- **Relevance:** Supports thesis that persistent user attributes should change outputs.

### 10. Consistency-Acceptability Divergence of LLMs in Judicial Decision-Making
- **Link:** [arxiv 2507.08881](https://arxiv.org/abs/2507.08881) (Jul 2025)
- **Methodology:** Meta-analysis + proposed Dual-Track Deliberative Multi-Role governance (judge, lawyer, litigant, public).
- **Cross-role?** Yes — stakeholder axis central.
- **Expected-divergence structure:** Partial — conceptual framework, not quantitative matrix.
- **Relevance:** Theoretical scaffolding (task × stakeholder grid) matches CrossSystemEval's matrix ambitions.

---

## Verification Note

Some arxiv IDs verified via search; papers in fast-moving 2025–2026 preprint space should be re-verified before citation.
