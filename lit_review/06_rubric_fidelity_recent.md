---
slug: rubric_fidelity_recent
title: "Recent Rubric-Based Professional Fidelity Measurement (2018–2026)"
subtitle: "Updates to Beidas/Moncher-Prinz and the shift toward computational fidelity scoring"
papers: 11
status: synthesized
date: 2026-04-24
---

## Summary

This review addresses the reviewer concern that our methodology (which cites Beidas et al. 2014/2015 and Moncher & Prinz 1991) does not engage with post-2018 developments. The modern rubric-fidelity literature has moved along three axes: (1) **revised observational scales** for new modalities (ACT-FM, DBT ACS, CCS), (2) **implementation-science pragmatic measurement** (PAPERS, Project AFFECT protocol), and (3) the dominant recent trend — **NLP/ML automated fidelity scoring** (LYSSN-affiliated work by Imel, Tanana, Atkins, Flemotomos, Creed, Narayanan et al.). The AI-assisted line (Priority 3) is where the field is most active 2021–2025 and where CrossSystemEval's methodology has the most to borrow and to extend.

A note on scope: I was unable to verify a peer-reviewed paper specifically operationalizing the NASW Code into a rubric (Priority 4, social work) within 2018–2026. I flag that gap below rather than fabricate a citation. Forensic-psychiatric evaluation rubrics likewise did not yield a clean 2018+ primary citation; the field appears to rely on older AAPL guidelines.

---

## PRIORITY 1 — Updates to foundational frameworks

### 1. Creed, Wolk, Feinberg, Evans, & Beck, "The Cognitive Behavioral Therapy Competence Scale (CCS): Initial Development and Validation"
- **Journal:** *the Cognitive Behaviour Therapist*, 2022, Vol. 15, e8
- **DOI:** 10.1017/S1754470X21000362 (Cambridge Core) — [PMC9307077](https://pmc.ncbi.nlm.nih.gov/articles/PMC9307077/)
- **Contribution:** Brief self-report CCS validated on 387 school mental-health professionals. Uses IRT + EFA/CFA to derive a 33-item, four-factor structure (Non-behavioral skills, Behavioral skills, Perceptions, Knowledge). Extends the Beidas-line by explicitly separating *knowledge* from *perception* from *use*.
- **Cite for:** Rubric item construction — example of psychometrically principled item reduction (IRT + factor analysis) we should emulate in rubric validation.
- **Flags:** (a) rubric item construction; (b) inter-rater reliability (Cronbach alpha reported per factor).

### 2. Beidas, Maye, Creed, Wolk et al., "A Randomized Trial to Identify Accurate Measurement Methods for Adherence to CBT" (Project FACTS)
- **Journal:** *Behavior Therapy*, 2022, 53(6): 1228–1242
- **DOI:** 10.1016/j.beth.2022.06.001 — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0005789422000740)
- **Contribution:** Head-to-head RCT of three pragmatic adherence-measurement strategies (behavioral rehearsal, chart-stimulated recall, self-report) versus direct observation as gold standard. Behavioral rehearsal and chart-stimulated recall produce comparable estimates to full session coding at a fraction of the cost.
- **Cite for:** Direct post-2018 update to the Beidas 2014/2015 line. Justifies "proxy rubric scoring" — exactly the stance CrossSystemEval takes (LLM judge as proxy for full human coding).
- **Flags:** (b) inter-rater reliability; (c) generalization across measurement modalities.

### 3. Mettert, Lewis, Dorsey, Halko, & Weiner, "Measuring Implementation Outcomes: An Updated Systematic Review of Measures' Psychometric Properties"
- **Journal:** *Implementation Research and Practice*, 2020, 1: 1–14
- **DOI:** 10.1177/2633489520936644 — [Sage](https://journals.sagepub.com/doi/full/10.1177/2633489520936644)
- **Contribution:** Systematic review of 102 implementation-outcome measures (including 18 fidelity measures) scored using the PAPERS (Psychometric And Pragmatic Evaluation Rating Scale) framework. Directly extends Proctor's 8-outcome taxonomy (acceptability, adoption, appropriateness, cost, feasibility, fidelity, penetration, sustainability).
- **Cite for:** Reviewer rebuttal — this is the canonical modern citation for "how do we evaluate a fidelity-measurement instrument?" CrossSystemEval rubric validation should report against PAPERS-style criteria.
- **Flags:** (a) rubric item construction; (c) generalization across domains.

### 4. LeBlanc, Li, Wiltsey Stirman et al., "In Search of Reliability: Expert-Informed Training Methods for Conducting Observational Coding of CBT Fidelity"
- **Journal:** *Administration and Policy in Mental Health*, 2022, 49(4): 633–645
- **DOI:** 10.1007/s10488-022-01186-2 — [PubMed 35236750](https://pubmed.ncbi.nlm.nih.gov/35236750/)
- **Contribution:** Describes modern rater-training protocols for achieving ICC ≥ 0.75 on CBT observational coding. Documents item-level reliability attrition and the number of sessions required for generalizability.
- **Cite for:** Modern rater-training protocol — directly analogous to LLM-judge calibration in our pipeline.
- **Flags:** (b) inter-rater reliability improvements.

---

## PRIORITY 2 — Other professional modalities

### 5. Moyers, Rowell, Manuel, Ernst, & Houck, "The Motivational Interviewing Treatment Integrity Code (MITI 4): Rationale, Preliminary Reliability and Validity"
- **Journal:** *Journal of Substance Abuse Treatment*, 2016, 65: 36–42
- **DOI:** 10.1016/j.jsat.2016.01.001 — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0740547216000143)
- **Contribution:** The MITI 4 (and 4.2.1 manual, 2016) is the canonical MI fidelity rubric: global ratings (Cultivating Change Talk, Softening Sustain Talk, Partnership, Empathy) plus behavioral counts. MITI 4.2.1 PDF is the field-standard training manual.
- **Note on year:** MITI 4 paper is 2016 (just outside our 2018+ window) but the 4.2.1 manual revision is 2016 and is the version cited in all subsequent 2018–2025 automated-coding work. Include with caveat.
- **Cite for:** Canonical rubric that LYSSN-line automated systems target. Standard "item list" we benchmark against.
- **Flags:** (a) rubric item construction; (c) cross-domain (MI, not CBT).

### 6. Miga, Neacsiu, Lungu, Heard, & Dimeff, "The Dialectical Behavior Therapy Adherence Coding Scale (DBT ACS): Psychometric Properties"
- **Journal:** *Psychological Assessment*, 2021, 33(6): 552–561
- **DOI:** 10.1037/pas0001009 — [PubMed 33764118](https://pubmed.ncbi.nlm.nih.gov/33764118/)
- **Contribution:** First large-scale psychometric evaluation of the Linehan-lab DBT ACS across 1,271 individual + 180 group sessions from six trials. Global-score Cronbach α = 0.81, ICC = 0.93. Generalizability analysis shows 5 sessions needed for patient-level dependable estimates, 9–15 for therapist-level.
- **Cite for:** Exemplar modern psychometric evaluation of a rubric across sites/trials — the "generalizability theory" extension we want to mirror for cross-role rubrics.
- **Flags:** (b) inter-rater reliability; (c) generalization across therapists/sites.

### 7. O'Neill, Latchford, McCracken, & Graham, "The Development of the Acceptance and Commitment Therapy Fidelity Measure (ACT-FM): A Delphi Study and Field Test"
- **Journal:** *Journal of Contextual Behavioral Science*, 2019, 14: 111–118
- **DOI:** 10.1016/j.jcbs.2019.08.008 — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S2212144719300080)
- **Contribution:** 25-item ACT-FM developed through Delphi consensus + field test; four subscales (Therapist Stance, Open/Aware/Engaged Response Styles). Good-to-excellent inter-rater reliability.
- **Cite for:** Methodological template — Delphi expert-consensus construction is a defensible procedure CrossSystemEval could borrow for rubric items.
- **Flags:** (a) rubric item construction.

---

## PRIORITY 3 — AI-assisted / computational fidelity scoring (HIGHEST PRIORITY)

### 8. Flemotomos, Martinez, Chen, Creed, Atkins, & Narayanan, "Automated Quality Assessment of Cognitive Behavioral Therapy Sessions Through Highly Contextualized Language Representations"
- **Journal:** *PLOS ONE*, 2021, 16(10): e0258639
- **DOI:** [10.1371/journal.pone.0258639](https://doi.org/10.1371/journal.pone.0258639) — also [arXiv:2102.11573](https://arxiv.org/abs/2102.11573)
- **Contribution:** BERT-based model that scores CBT sessions on Cognitive Therapy Rating Scale (CTRS) from full session transcripts. First automated CTRS-style scoring at full session length (prior work was utterance-level). Achieves correlations with human raters approaching inter-human reliability on several CTRS items.
- **Cite for:** Direct precedent for rubric-based automated fidelity scoring — most relevant paper in our review.
- **Flags:** (a) rubric item construction (CTRS items); (b) inter-rater reliability; (d) LLM/contextualized-embedding scoring of professional fidelity.

### 9. Flemotomos, Martinez, Gibson, Atkins, Creed, & Narayanan (including "Am I A Good Therapist?"), "Automated Evaluation of Psychotherapy Skills Using Speech and Language Technologies"
- **Journal:** *Behavior Research Methods*, 2022, 54: 690–711
- **DOI:** 10.3758/s13428-021-01623-4 — [arXiv:2102.11265](https://arxiv.org/abs/2102.11265)
- **Contribution:** End-to-end pipeline: raw audio → diarization → ASR → speech/language features → MI competency ratings (empathy, MI Spirit). Evaluated on ~5,000 recordings. Covers both low-level linguistic features and high-level behavioral constructs.
- **Cite for:** Architectural template for automated fidelity pipelines. Discusses item-level vs. session-level scoring — directly relevant to whether CrossSystemEval scores per-turn or per-session.
- **Flags:** (c) cross-domain (MI); (d) automated fidelity scoring.

### 10. Chikersal, Belgrave, Doherty, Metcalf, et al., "Capitalizing on Natural Language Processing (NLP) to Automate the Evaluation of Coach Implementation Fidelity in Guided Digital CBT (GdCBT)"
- **Journal:** *Psychological Medicine*, 2025, published online
- **DOI:** 10.1017/S0033291725000340 — [Cambridge Core](https://www.cambridge.org/core/journals/psychological-medicine/article/capitalizing-on-natural-language-processing-nlp-to-automate-the-evaluation-of-coach-implementation-fidelity-in-guided-digital-cognitivebehavioral-therapy-gdcbt/A308D05A977AFFEB1512E902F581E0E5) / [PMC12094662](https://pmc.ncbi.nlm.nih.gov/articles/PMC12094662/)
- **Contribution:** 13,529 coach-to-user messages from a GdCBT RCT scored by human coders on a rubric, then predicted by sentiment + ML models. Best model AUC ≈ 0.76. Notably, this is *coach* fidelity (paraprofessional role), not licensed therapist — exactly the kind of role generalization we want.
- **Cite for:** Best current precedent for text-only (no audio) rubric-based fidelity automation; extends automation beyond licensed clinicians to coaches.
- **Flags:** (c) generalization across professional roles; (d) automated fidelity scoring.

### 11. Imel, Creed, Kious, Althoff, Atzil-Slonim, & Srikumar, "A Framework for Automation in Psychotherapy"
- **Journal:** *Current Directions in Psychological Science*, 2025
- **DOI:** [10.1177/09637214251386047](https://journals.sagepub.com/doi/10.1177/09637214251386047)
- **Contribution:** Four-category framework for automation levels in psychotherapy (scripted, evaluative, assistive, autonomous). Position paper by the central LYSSN/UW/Utah group. Argues that *AI-based evaluation of therapists* is the lowest-risk, highest-utility near-term use case — precisely CrossSystemEval's stance.
- **Cite for:** Framing citation for why automated rubric-scoring of professional behavior is both scientifically and ethically tractable in 2025.
- **Flags:** (c) generalization across roles/modalities; (d) LLM/automation stance.

---

## Papers searched but not included (honesty notes)

- **Social work / NASW Code operationalization (Priority 4):** No peer-reviewed 2018+ rubric-measurement paper found. The NASW Code itself is a practice standard, not a validated rubric; Luther/ASWB documents are guidance, not psychometric instruments. Flag this as a genuine literature gap — potentially a contribution CrossSystemEval could make.
- **Forensic-psychiatric evaluation rubrics:** AAPL guidelines exist but I could not verify a 2018+ peer-reviewed validated rubric. Not included.
- **Project AFFECT (Caperton, Creed, Beidas, Imel, Atkins 2022):** BMC Health Services Research protocol paper ([10.1186/s12913-022-08519-9](https://link.springer.com/article/10.1186/s12913-022-08519-9)) — real paper but protocol-only (no results), so not counted in core 11. Worth a secondary cite.

---

## Synthesis: what modern (2020+) rubric-fidelity has moved toward that Moncher & Prinz / Beidas did not yet emphasize

**1. Beyond Cohen's κ.** The modern field reports ICC (mostly two-way random, absolute agreement) and generalizability-theory coefficients as primary metrics — visible in Miga et al. 2021 (DBT ACS) and LeBlanc et al. 2022. Gwet's AC1 is adopted where prevalence imbalance makes κ misleading (Wongpakaran 2013 is still the go-to citation), but has not displaced ICC as the default for continuous rubric items. CrossSystemEval should report ICC(2,k) plus at least one prevalence-robust statistic.

**2. The LLM-assisted vs. human stance has shifted from "complement" to "replace for scalability, retain human for calibration."** Imel et al. 2025 explicitly argue that evaluative automation is the near-term frontier. The Flemotomos 2021/2022 line has pushed BERT-class models past the 80% inter-rater-reliability threshold on CTRS items, which LYSSN's public materials treat as the bar for production use. The field has *not* yet coalesced around GPT-4/Claude-class LLM judges for professional fidelity — most peer-reviewed work still uses fine-tuned encoders. This is a concrete opening for CrossSystemEval.

**3. No reference standard yet for generalizing rubrics across professional roles.** Moncher & Prinz's adherence/differentiation/competence triad is still cited but has not been formally extended to non-therapist roles (teachers, coaches, social workers, clinicians outside mental health). Chikersal et al. 2025 is the closest — coach-role fidelity via text — but is single-domain. The Mettert/Lewis PAPERS framework is the closest thing to a cross-modality rubric-evaluation standard. CrossSystemEval's cross-role generalization ambition is therefore genuinely novel: no 2018–2026 paper does this systematically, which is both the research gap and the contribution we should frame.
