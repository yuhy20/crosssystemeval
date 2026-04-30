---
slug: mental-health-ai
title: "Mental Health AI Evaluation (Commitment, Crisis, Forensic)"
subtitle: "Verified citations on LLM evaluation in psychiatric, forensic, and crisis contexts"
papers: 14
status: verified — every entry confirmed via primary source fetch
date: 2026-04-27
---

## Summary

This rebuilt review replaces a prior version in which roughly half the citations were confabulated (see `04_mental_health_ai_evals.md` git history; specifically Wagner/Hassan/Lee 2025, Levkovich & Elyoseph 2025 on C-SSRS, Park/Desai/Kumar "CrisisBench" 2024, Gupta et al. "SafetyBench-MH" 2025, Patel/Browne/Varga 2025, Chen et al. 2025 "Role-Play Fidelity in LLM-Simulated Psychiatric Patients", and Ramirez et al. 2025 — all confirmed not to exist on arxiv/PubMed/DOI). What follows includes only papers I personally fetched and confirmed.

### What real benchmarks/evals exist

**Psychiatric clinical/diagnostic benchmarks (real):**
- **PsychiatryBench** (Fouda et al. 2025, arxiv 2509.09711) — 5,188 expert-annotated items across 11 psychiatric tasks.
- **PsychBench** (Liu et al. 2025, arxiv 2503.01903) — 16-LLM evaluation grounded in real Chinese psychiatric clinical data, with a 60-psychiatrist clinical study.
- **MentalBench** (Song et al. 2026, arxiv 2602.12871) — DSM-5-grounded knowledge graph with ~24,750 synthetic cases for diagnostic reasoning. *Note: original review described this as "MentalBench-100k" with multi-turn dialogues — that was wrong. The real "100k" benchmark is Badawi et al.'s separate work below.*
- **MentalBench-100k / MentalAlign-70k** (Badawi et al. 2025, arxiv 2510.19032) — 100K LLM response pairs over real therapy conversations; finds LLM judges systematically inflate ratings, especially for empathy and safety.
- **CounselBench** (Li et al. 2025, arxiv 2506.08584) — 100 mental-health professionals, 2,000 expert evaluations, adversarial counseling-QA dataset.
- **MentaLLaMA** (Yang et al. 2023, arxiv 2309.13567) — foundational interpretable mental-health analysis benchmark (105K-sample IMHI dataset).

**Crisis / suicide-risk evaluation (real):**
- **Schoene & Canca** (2025, arxiv 2507.02990) — jailbreaking LLMs in suicide/self-harm contexts; 5/6 models breached in <2 turns.
- **Patil, Tao, Gedhu** (2025, arxiv 2505.13480) — C-SSRS-aligned LLM suicide-risk classification on r/SuicideWatch.
- **Arnaiz-Rodriguez et al.** (2025, arxiv 2509.24857) — 2,000-input crisis-handling benchmark, six-category taxonomy.
- **Shah et al.** (2025, arxiv 2509.08839) — clinician-developed framework, six LLMs on crisis-disclosure response.
- **Donnelly et al.** (2025, medRxiv) — LLM-based safety-plan fidelity scoring (SPIFR) on 266 plans.
- **Thotapalli et al.** (2025, PCN Reports / PMID 40673126) — psychiatric emergency triage, GPT-4 vs. clinicians, 22 vignettes; tendency to over-triage admission.

**Stigma / role / persona safety (real):**
- **Moore et al.** (2025, arxiv 2504.18412) — LLMs express stigma toward schizophrenia/alcohol-dependence > depression; encourage delusional thinking via sycophancy.
- **MHSafeEval** (Lee et al. 2026, arxiv 2604.17730) — *role-aware* mental-health safety evaluation; defines harm-typology roles (perpetrator, instigator, facilitator, enabler) the AI counselor adopts.
- **Liang et al.** (2025, arxiv 2510.24677) — neuronal-ablation analysis showing prompt-based clinical role-playing changes surface style but **not** underlying reasoning pathways.
- **Zhao et al.** (2024, arxiv 2409.13979) — "Role-Play Paradox": role-playing in LLMs amplifies bias and produces unsafe outputs even with neutral roles.

**Methodological precedent (real):**
- **MedAgents** (Tang et al. 2023, arxiv 2311.10537) — multi-agent role-playing for medical reasoning (gather domain experts → individual analyses → consensus). ACL 2024 Findings.
- **MedAgentBench** (Jiang et al. 2025, arxiv 2501.14654) — 300 EHR-grounded agent tasks with FHIR APIs. *Note: previous review mis-described this as multi-role attending/resident/nurse — that was wrong. It is single-agent EHR navigation.*
- **AI Hospital** (Fan et al. 2024, arxiv 2402.09742) — multi-role medical interaction simulator (Doctor / Patient / Examiner / Chief Physician).
- **AgentClinic** (Schmidgall et al. 2024, arxiv 2405.07960) — multimodal patient-doctor-measurement-moderator simulator with embedded cognitive biases.
- **CARES** (Chen et al. 2025, arxiv 2505.11413) — 18,000-prompt medical-LLM safety benchmark; *role-play* is one of four prompting styles tested.
- **Ke et al.** (2024, JMIR) — multi-agent LLM conversations to mitigate cognitive biases in clinical decisions; 0% → 76% accuracy on 16 misdiagnosis cases.

### Genuine gaps (no published LLM evaluation work found)

These are the gaps CrossSystemEval can legitimately claim:

1. **No LLM evaluation specific to AOT / Kendra's Law / Baker Act / LPS Act.** Searches across arxiv, PubMed, and Google Scholar surfaced no benchmark, vignette study, or scoping review of LLM behavior on involuntary outpatient or inpatient commitment statutes. Capacity-assessment and involuntary-commitment review articles exist (e.g., the Springer scoping review on (in)voluntary terminology, 2025) but contain no LLM evaluation component.
2. **No LLM-on-forensic-psychiatry benchmark.** The Sciencedirect "case study of forensic psychiatry experts' reports" (S016025272500055X) uses GPT-4o to extract variables *from* forensic reports — it does not evaluate LLMs as forensic decision-makers on competency / NGRI / civil commitment.
3. **No mandated-reporter LLM benchmark.** No paper found testing LLMs on Tarasoff / CPS / APS / IPV reporting decisions across professional role frames. The Wagner/Hassan/Lee (2025) JAMA Network Open paper cited in the prior review does not exist.
4. **No same-scenario, different-professional-role mental-health benchmark.** MHSafeEval (the closest) studies interactional roles the *AI counselor* takes, not different *user professional roles* presenting the same scenario. AI Hospital and MedAgents use multi-role agents but for cooperative diagnosis, not comparative role-fidelity. Liang et al. 2025 (arxiv 2510.24677) shows prompt-based role conditioning is largely cosmetic — directly relevant motivation for CrossSystemEval.

### Strongest methodological precedent actually found

The closest legitimate methodological precedents for CrossSystemEval are:

1. **Liang et al. 2025 (arxiv 2510.24677)** — empirically shows that current prompt-based clinical role-playing *fails* to produce real cognitive differentiation. This is directly load-bearing: it both motivates CrossSystemEval (we need to test whether role framing matters) and warns it (the answer may be that LLMs collapse role distinctions even in higher-stakes contexts).
2. **MHSafeEval / Lee et al. 2026 (arxiv 2604.17730)** — "role-aware" safety evaluation in mental-health LLMs, though "role" here means the harm-role the counselor occupies, not the user's professional role.
3. **AgentClinic (Schmidgall et al. 2024, arxiv 2405.07960)** — closest design pattern: scenario presented across multiple agent perspectives (doctor / patient / measurement / moderator) with embedded biases. Diagnostic accuracy drops >10× under sequential role interaction.

For positioning, the safest claim CrossSystemEval can make is: *"The first benchmark to test cross-role professional fidelity (patient / family / therapist / police / social worker / judge) for LLM behavior under a specific involuntary-commitment statute (NY MHL §9.60 / Kendra's Law). Prior role-conditioned LLM evaluations either (a) test the role the AI takes [MHSafeEval], (b) test cooperative multi-role diagnosis [MedAgents, AI Hospital], or (c) show prompt-based role framing is largely cosmetic [Liang et al.]. None tests the same statutory commitment scenario across different requesting-professional frames."*

---

## Papers

### 1. PsychiatryBench: A Multi-Task Benchmark for LLMs in Psychiatry
- **Authors:** Aya E. Fouda, Abdelrahmn A. Hassan, Radwa J. Hanafy, Mohammed E. Fouda
- **Venue:** arxiv 2509.09711, submitted Sep 7 2025 (v2: Nov 23 2025); accepted at npj Digital Medicine
- **URL:** https://arxiv.org/abs/2509.09711 (verified)
- **Methodology:** 5,188 expert-annotated items across 11 QA tasks (diagnostic reasoning, treatment planning, longitudinal follow-up, sequential case analysis), grounded in expert-validated psychiatric textbooks and casebooks.
- **Cross-role?** No.
- **Relevance:** Most rigorous current general-psychiatry LLM benchmark. Does *not* address commitment, forensics, or role variation, but is the canonical reference for "what a serious psychiatry-LLM benchmark looks like."

### 2. PsychBench: A Comprehensive Benchmark for LLM-Assisted Psychiatric Clinical Practice
- **Authors:** Shuyu Liu, Ruoxi Wang, Ling Zhang, Xuequan Zhu, Rui Yang, Xinzhu Zhou, Fei Wu, Zhi Yang, Cheng Jin, Gang Wang
- **Venue:** arxiv 2503.01903, submitted Feb 28 2025
- **URL:** https://arxiv.org/abs/2503.01903 (verified)
- **Methodology:** 16-LLM evaluation across psychiatric clinical tasks; clinical study with 60 psychiatrists rating practical utility; tests prompt design, CoT, text length, fine-tuning effects.
- **Cross-role?** Stratifies by clinician experience level (junior vs. senior psychiatrist evaluators) but not by user professional role.
- **Relevance:** Establishes that LLMs are "auxiliary" for junior psychiatrists but "not yet adequate as decision-making tools." Useful for situating CrossSystemEval against a strong existing clinical benchmark.

### 3. MentalBench: Evaluating Psychiatric Diagnostic Capability of LLMs
- **Authors:** Hoyun Song, Migyeong Kang, Jisu Shin, Jihyun Kim, Chanbi Park, Hangyeol Yoo, Jihyun An, Alice Oh, Jinyoung Han, KyungTae Lim
- **Venue:** arxiv 2602.12871, submitted Feb 13 2026
- **URL:** https://arxiv.org/abs/2602.12871 (verified)
- **Methodology:** MentalKG knowledge graph encoding DSM-5 criteria for 23 conditions; ~24,750 synthetic clinical cases varying information completeness and difficulty.
- **Cross-role?** No.
- **Relevance:** Important to cite to *correct the previous review's mis-identification* (it is not "MentalBench-100k" with multi-turn dialogues). Real finding: LLMs are strong on structured DSM-5 queries but poorly calibrated on overlapping disorders.

### 4. When Can We Trust LLMs in Mental Health? (MentalBench-100k / MentalAlign-70k)
- **Authors:** Abeer Badawi, Elahe Rahimi, Md Tahmid Rahman Laskar, Sheri Grach, Lindsay Bertrand, Lames Danok, Jimmy Huang, Frank Rudzicz, Elham Dolatabadi
- **Venue:** arxiv 2510.19032, submitted Oct 21 2025; EACL 2026
- **URL:** https://arxiv.org/abs/2510.19032 (verified)
- **Methodology:** 10,000 single-session real therapy conversations × 9 LLM responses = 100,000 pairs (MentalBench-100k); 70,000 ratings comparing 4 LLM-judges to human experts on 7 attributes (MentalAlign-70k).
- **Cross-role?** No.
- **Relevance:** Critical methodological caution: LLM judges systematically inflate ratings, are unreliable for empathy and safety. CrossSystemEval should rely on human or rubric-based evaluation rather than LLM-as-judge for safety-critical commitment dimensions.

### 5. CounselBench: Expert Evaluation and Adversarial Benchmarking of LLMs in Mental-Health QA
- **Authors:** Yahan Li, Jifan Yao, John Bosco S. Bunyi, Adam C. Frank, Angel Hsing-Chi Hwang, Ruishan Liu
- **Venue:** arxiv 2506.08584, submitted Jun 10 2025
- **URL:** https://arxiv.org/abs/2506.08584 (verified)
- **Methodology:** 100 mental-health professionals; 2,000 expert evaluations; adversarial dataset for failure-pattern extraction.
- **Cross-role?** No.
- **Relevance:** Real adversarial-evaluation precedent. Same expert-recruitment scale CrossSystemEval might emulate.

### 6. MentaLLaMA: Interpretable Mental Health Analysis on Social Media
- **Authors:** Kailai Yang, Tianlin Zhang, Ziyan Kuang, Qianqian Xie, Jimin Huang, Sophia Ananiadou
- **Venue:** arxiv 2309.13567, submitted Sep 24 2023; ACM Web Conference 2024
- **URL:** https://arxiv.org/abs/2309.13567 (verified)
- **Methodology:** 105K-sample IMHI dataset over 8 mental-health tasks from 10 social-media sources; first open-source instruction-following LLM for interpretable mental-health analysis.
- **Cross-role?** No.
- **Relevance:** Foundational, often-cited. Establishes the social-media-mental-health task taxonomy CrossSystemEval can position against.

### 7. Jailbreaking LLMs in Suicide and Self-Harm Contexts
- **Authors:** Annika M. Schoene, Cansu Canca
- **Venue:** arxiv 2507.02990, submitted Jul 1 2025
- **URL:** https://arxiv.org/abs/2507.02990 (verified)
- **Methodology:** Multi-step prompt-injection jailbreaks across six LLMs in suicide/self-harm scenarios; 5/6 models produce detailed harmful content within <2 turns.
- **Cross-role?** No (the abstract does not center role/persona variation as the attack vector).
- **Relevance:** Strongest published finding that current LLM safety filters are brittle in mental-health crisis prompts. Justifies why role-conditioned commitment scenarios may also bypass safety training.

### 8. Evaluating Reasoning LLMs for Suicide Screening with the C-SSRS
- **Authors:** Avinash Patil, Siru Tao, Amardeep Gedhu
- **Venue:** arxiv 2505.13480, submitted May 11 2025
- **URL:** https://arxiv.org/abs/2505.13480 (verified)
- **Methodology:** Six models (Claude, GPT, Mistral, LLaMA variants) zero-shot classifying ~1,200 r/SuicideWatch posts on the C-SSRS 7-point severity scale.
- **Cross-role?** No.
- **Relevance:** This is the *real* C-SSRS / LLM paper (replacing the confabulated Levkovich & Elyoseph 2025 entry from the previous review). Misclassifications cluster between adjacent severity levels — relevant precedent for graded commitment-threshold rubrics.

### 9. Between Help and Harm: Evaluation of Mental Health Crisis Handling by LLMs
- **Authors:** Adrian Arnaiz-Rodriguez, Miguel Baidal, Erik Derner, Jenn Layton Annable, Mark Ball, Mark Ince, Elvira Perez Vallejos, Nuria Oliver
- **Venue:** arxiv 2509.24857, submitted Sep 29 2025
- **URL:** https://arxiv.org/abs/2509.24857 (verified)
- **Methodology:** Six-category crisis taxonomy; >2,000 inputs; five LLMs scored on 5-point safety scale.
- **Cross-role?** No (abstract does not mention role variation, mandated reporting, or commitment).
- **Relevance:** Closest extant "crisis benchmark" — replacing the confabulated Park/Desai/Kumar "CrisisBench" from the previous review. Models are weakest on self-harm and suicidal ideation.

### 10. Evaluating Clinical Safety of LLMs in High-Risk Mental Health Disclosures
- **Authors:** Siddharth Shah, Amit Gupta, Aarav Mann, Alexandre Vaz, Benjamin E. Caldwell, Robert Scholz, Peter Awad, Rocky Allemandi, Doug Faust, Harshita Banka, Tony Rousmaniere
- **Venue:** arxiv 2509.08839, submitted Sep 1 2025
- **URL:** https://arxiv.org/abs/2509.08839 (verified)
- **Methodology:** Six LLMs scored by clinicians on five safety behaviors (risk acknowledgment, empathy, professional-help encouragement, resource provision, sustained engagement).
- **Cross-role?** No.
- **Relevance:** Direct rubric precedent. Claude leads; Grok/ChatGPT/LLaMA underperform; none meets clinical standard.

### 11. Expressing Stigma and Inappropriate Responses Prevents LLMs from Safely Replacing Mental-Health Providers
- **Authors:** Jared Moore, Declan Grabb, William Agnew, Kevin Klyman, Stevie Chancellor, Desmond C. Ong, Nick Haber
- **Venue:** arxiv 2504.18412, submitted Apr 25 2025
- **URL:** https://arxiv.org/abs/2504.18412 (verified)
- **Methodology:** Vignette-based testing; therapy-chatbots and frontier LLMs given persona-prompted "expert therapist" instructions, then evaluated for stigma toward conditions and appropriateness on critical scenarios (delusions, suicidality).
- **Cross-role?** Partially — the AI is asked to take an "expert therapist" persona, but the *user-presented* role does not vary.
- **Relevance:** Demonstrates **two role-conditioned safety failures** directly relevant to commitment scenarios: (a) differential stigma (more toward schizophrenia/alcohol-dependence than depression) and (b) sycophantic encouragement of delusional thinking. Both are exactly the failure modes that matter under §9.60 evaluation, where "lack of insight" + delusion is the legal trigger.

### 12. MHSafeEval: Role-Aware Interaction-Level Evaluation of Mental Health Safety
- **Authors:** Suhyun Lee, Palakorn Achananuparp, Neemesh Yadav, Ee-Peng Lim, Yang Deng
- **Venue:** arxiv 2604.17730, submitted Apr 20 2026
- **URL:** https://arxiv.org/abs/2604.17730 (verified)
- **Methodology:** R-MHSafe taxonomy classifying AI-counselor harm by interactional role (perpetrator / instigator / facilitator / enabler); agent-based adversarial multi-turn evaluation framework.
- **Cross-role?** **Yes — but a different sense of "role" than CrossSystemEval.** "Role" here is the harm-role the *AI counselor* adopts in interaction, not the role of the *user* presenting a scenario.
- **Relevance:** Closest published "role-aware" mental-health safety benchmark. The taxonomy is reusable (an AI that "facilitates" inappropriate involuntary commitment vs. one that "enables" denial of needed care is exactly the harm pattern CrossSystemEval should detect). Substantive distinction from CrossSystemEval is worth making explicit in the paper.

### 13. Dissecting Role Cognition in Medical LLMs via Neuronal Ablation
- **Authors:** Xun Liang, Huayi Lai, Hanyu Wang, Wentao Zhang, Linfeng Zhang, Yanfang Chen, Feiyu Xiong, Zhiyu Li
- **Venue:** arxiv 2510.24677, submitted Oct 28 2025
- **URL:** https://arxiv.org/abs/2510.24677 (verified)
- **Methodology:** Neuronal-ablation analysis of Prompt-Based Role Playing (PBRP) where models adopt clinical roles (medical student / resident / attending). Tests whether role prompts induce distinct reasoning pathways.
- **Cross-role?** **Yes, directly.** This is the most relevant single paper for CrossSystemEval's hypothesis.
- **Relevance:** **Top-3 paper for positioning.** Empirical finding: "role prompts do not significantly enhance medical reasoning… they primarily affect surface-level linguistic features." Core decision-making mechanisms are *uniform across roles*. This is both the strongest motivation for CrossSystemEval (current role-conditioning is shallow) and a warning that we may find LLMs collapse all six professional roles to the same answer. CrossSystemEval should design specifically to detect this collapse.

### 14. Role-Play Paradox in LLMs: Reasoning Performance Gains and Ethical Dilemmas
- **Authors:** Jinman Zhao, Zifan Qian, Linbo Cao, Yining Wang, Yitian Ding, Yulan Hu, Zeyu Zhang, Zeyong Jin
- **Venue:** arxiv 2409.13979, submitted Sep 21 2024 (revised Feb 3 2025)
- **URL:** https://arxiv.org/abs/2409.13979 (verified)
- **Methodology:** Bias evaluation across role-conditioned LLMs on stereotype benchmarks; auto-tuned role selection vs. explicit assignment.
- **Cross-role?** **Yes** — role variation is the central manipulation.
- **Relevance:** Empirically establishes that "role-play consistently amplifies the risk of biased outputs," even when the assigned role is neutral. CrossSystemEval should report bias outputs by role explicitly to characterize amplification under commitment-decision framing.

---

## Methodological-precedent papers (non-mental-health-specific but architecturally relevant)

### 15. MedAgents: LLMs as Collaborators for Zero-Shot Medical Reasoning
- **Authors:** Xiangru Tang, Anni Zou, Zhuosheng Zhang, Ziming Li, Yilun Zhao, Xingyao Zhang, Arman Cohan, Mark Gerstein
- **Venue:** arxiv 2311.10537, submitted Nov 16 2023; ACL 2024 Findings
- **URL:** https://arxiv.org/abs/2311.10537 (verified)
- **Methodology:** Multi-agent role-playing pipeline (gather domain experts → individual analyses → synthesize report → iterate to consensus → decide); 9 medical datasets including MedQA, MedMCQA.
- **Cross-role?** Yes — multi-role, but cooperative consensus-seeking, not comparative role fidelity.
- **Relevance:** Canonical citation for multi-agent medical role-playing. CrossSystemEval is *architecturally inverted* — same scenario, different roles, looking for divergence rather than convergence.

### 16. AI Hospital: Multi-Agent Medical Interaction Simulator
- **Authors:** Zhihao Fan, Jialong Tang, Wei Chen, Siyuan Wang, Zhongyu Wei, Jun Xi, Fei Huang, Jingren Zhou
- **Venue:** arxiv 2402.09742, submitted Feb 15 2024
- **URL:** https://arxiv.org/abs/2402.09742 (verified)
- **Methodology:** Doctor / Patient / Examiner / Chief Physician roles in dynamic simulation; Multi-View Medical Evaluation benchmark on Chinese medical records.
- **Cross-role?** Yes — multi-role, with NPC roles around a Doctor agent.
- **Relevance:** Strongest existing multi-role architectural precedent in clinical care. Cross-role design principle (different agents have different information) is borrowable.

### 17. AgentClinic: Multimodal Agent Benchmark for Simulated Clinical Environments
- **Authors:** Samuel Schmidgall, Rojin Ziaei, Carl Harris, Eduardo Reis, Jeffrey Jopling, Michael Moor
- **Venue:** arxiv 2405.07960, submitted May 13 2024
- **URL:** https://arxiv.org/abs/2405.07960 (verified)
- **Methodology:** Doctor agent uncovers diagnosis through dialogue with patient agent + tools (measurement, moderator); embeds cognitive/implicit biases in both patient and doctor agents.
- **Cross-role?** Yes (doctor / patient / measurement / moderator), and explicitly studies bias under role.
- **Relevance:** Closest design pattern. Demonstrated that bias injection produces large diagnostic-accuracy drops — provides a precedent for measuring degradation under role manipulation.

### 18. CARES: Comprehensive Evaluation of Safety and Adversarial Robustness in Medical LLMs
- **Authors:** Sijia Chen, Xiaomin Li, Mengxue Zhang, Eric Hanchen Jiang, Qingcheng Zeng, Chen-Hsiang Yu
- **Venue:** arxiv 2505.11413, submitted May 16 2025
- **URL:** https://arxiv.org/abs/2505.11413 (verified)
- **Methodology:** 18,000 prompts × 8 medical-safety principles × 4 harm levels × 4 prompting strategies (direct / indirect / obfuscated / **role-play**); three-way Accept/Caution/Refuse protocol.
- **Cross-role?** Partial — role-play is one of four prompting styles, not the dominant axis.
- **Relevance:** Already-published precedent for treating role-play as a structured evaluation dimension in medical-LLM safety. Their Safety Score metric and three-way refusal protocol are reusable.

### 19. MedAgentBench: Realistic Virtual EHR Environment for Medical LLM Agents
- **Authors:** Yixing Jiang, Kameron C. Black, Gloria Geng, Danny Park, James Zou, Andrew Y. Ng, Jonathan H. Chen
- **Venue:** arxiv 2501.14654, submitted Jan 24 2025
- **URL:** https://arxiv.org/abs/2501.14654 (verified)
- **Methodology:** 300 physician-written EHR-grounded tasks across 10 categories; 100-patient FHIR-API EHR environment; best model ~70%.
- **Cross-role?** **No.** *Important correction*: previous review described this as "multi-role attending/resident/nurse/pharmacist/patient across 14 specialties" — that description was confabulated. The actual paper is a single-agent EHR-task benchmark.
- **Relevance:** Architectural precedent for grounding in real clinical infrastructure. Not directly about role variation.

### 20. Mitigating Cognitive Biases via Multi-Agent LLM Conversations
- **Authors:** Yuhe Ke, Rui Yang, Sui An Lie, Taylor Xin Yi Lim, Yilin Ning, Irene Li, Hairil Rizal Abdullah, Daniel Shu Wei Ting, Nan Liu
- **Venue:** Journal of Medical Internet Research 26 (2024), Nov 19 2024
- **URL:** https://www.jmir.org/2024/1/e59439 (verified)
- **Methodology:** GPT-4 multi-agent conversations on 16 case reports with cognitive-bias-driven misdiagnoses; targeting anchoring, confirmation, premature-closure biases.
- **Cross-role?** Yes — multi-agent debiasing roles.
- **Relevance:** Demonstrates that multi-agent role debate *can* improve clinical accuracy (0% → 76%), counterbalancing Liang et al.'s pessimistic finding. Useful for arguing CrossSystemEval results may differ if architecture is dialogic rather than single-prompt.

---

## Topic-by-topic gap summary

| Sub-area | Real published LLM eval? | Notes |
|---|---|---|
| Psychiatric clinical / diagnostic benchmarks | YES — PsychiatryBench, PsychBench, MentalBench, MentalBench-100k, CounselBench, MentaLLaMA | Saturated. CrossSystemEval should not duplicate. |
| LLM crisis / suicide-risk evaluation | YES — Schoene & Canca, Patil et al. (C-SSRS), Arnaiz-Rodriguez, Shah et al., Donnelly et al. (SPIFR), Thotapalli et al. | Mature sub-area; CrossSystemEval can reference but does not need to extend. |
| LLM forensic-psychiatry decision-making | **NO** | Sciencedirect S016025272500055X uses LLMs to extract data *from* forensic reports; does not evaluate LLM forensic reasoning. **GENUINE GAP.** |
| LLM evaluation under involuntary commitment / AOT / Kendra's Law / Baker Act / LPS | **NO** | No benchmark, vignette study, or scoping review found. **GENUINE GAP — the strongest CrossSystemEval claim.** |
| Mandated-reporter LLM evaluation (Tarasoff / CPS / APS / IPV) | **NO** | The Wagner/Hassan/Lee 2025 JAMA Network Open paper claimed in the prior review does not exist. **GENUINE GAP.** |
| Cross-role LLM evaluation (same scenario, different professional user) | **NO** | MHSafeEval studies AI-counselor harm-roles, not user-professional roles. AI Hospital / MedAgents / AgentClinic use multi-role agents cooperatively, not comparatively. **GENUINE GAP.** |
| Role-conditioning bias / sycophancy / persona-induced safety failures | YES — Liang et al., Zhao et al. (Role-Play Paradox), Moore et al. (stigma), MHSafeEval | Mature; provides motivation for CrossSystemEval but does not occupy the gap. |
| Multi-agent / role-conditioned medical LLM benchmarks (methodological) | YES — MedAgents, AI Hospital, AgentClinic, MedAgentBench, CARES, Ke et al. | Used as architectural precedent. |

---

## Verification log

Every URL below was personally fetched and confirmed during this rebuild.

| URL | Result |
|---|---|
| https://arxiv.org/abs/2602.12871 | 200 OK — MentalBench (Song et al. 2026), DSM-5 KG, ~24,750 cases. **Note**: previous review's "MentalBench-100k multi-turn" description was wrong. |
| https://arxiv.org/abs/2501.14654 | 200 OK — MedAgentBench (Jiang et al. 2025), EHR/FHIR agent benchmark. **Note**: previous review's "multi-role attending/resident/nurse" description was wrong. |
| https://arxiv.org/abs/2505.13480 | 200 OK — Patil/Tao/Gedhu, C-SSRS LLM eval, May 2025. |
| https://arxiv.org/abs/2308.01834 | 200 OK — Galatzer-Levy et al. 2023, Med-PaLM 2 psychiatric functioning. (Found but not included; older, more general.) |
| https://arxiv.org/abs/2510.19032 | 200 OK — Badawi et al., MentalBench-100k / MentalAlign-70k, Oct 2025. |
| https://arxiv.org/abs/2506.08584 | 200 OK — Li et al., CounselBench, Jun 2025. |
| https://arxiv.org/abs/2509.24857 | 200 OK — Arnaiz-Rodriguez et al., crisis-handling, Sep 2025. |
| https://arxiv.org/abs/2504.18412 | 200 OK — Moore et al., stigma + delusion-encouragement, Apr 2025. |
| https://arxiv.org/abs/2604.17730 | 200 OK — MHSafeEval (Lee et al. 2026), role-aware harm taxonomy. |
| https://arxiv.org/abs/2510.24677 | 200 OK — Liang et al., neuronal ablation of role cognition, Oct 2025. |
| https://arxiv.org/abs/2409.13979 | 200 OK — Zhao et al., Role-Play Paradox, Sep 2024. |
| https://arxiv.org/abs/2311.10537 | 200 OK — Tang et al., MedAgents, Nov 2023 / ACL 2024. |
| https://arxiv.org/abs/2402.09742 | 200 OK — Fan et al., AI Hospital, Feb 2024. |
| https://arxiv.org/abs/2405.07960 | 200 OK — Schmidgall et al., AgentClinic, May 2024. |
| https://arxiv.org/abs/2505.11413 | 200 OK — Chen et al., CARES, May 2025; explicitly tests role-play prompts. |
| https://arxiv.org/abs/2509.09711 | 200 OK — Fouda et al., PsychiatryBench, Sep 2025. |
| https://arxiv.org/abs/2503.01903 | 200 OK — Liu et al., PsychBench, Feb 2025. |
| https://arxiv.org/abs/2309.13567 | 200 OK — Yang et al., MentaLLaMA, Sep 2023 / WWW 2024. |
| https://arxiv.org/abs/2507.02990 | 200 OK — Schoene & Canca, jailbreaking suicide/self-harm, Jul 2025. |
| https://arxiv.org/abs/2509.08839 | 200 OK — Shah et al., high-risk MH disclosure clinical safety, Sep 2025. |
| https://arxiv.org/abs/2501.01594 | 200 OK — PSYCHE (Lee et al. 2025), patient-simulation framework. (Found but not included; less directly relevant to commitment.) |
| https://arxiv.org/abs/2405.19660 | 200 OK — PATIENT-Ψ (Wang et al. 2024), CBT patient simulation. (Found but not included; tangential.) |
| https://www.jmir.org/2024/1/e59439 | 200 OK — Ke et al., multi-agent debiasing, JMIR Nov 2024. |
| https://www.jmir.org/2025/1/e87367 | 200 OK — Clegg, "Shoggoths, Sycophancy, Psychosis" commentary, JMIR Nov 2025. (Found but not numbered as a primary paper; commentary, not original eval.) |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC11974942/ | 200 OK — Donnelly et al., SPIFR safety-plan scoring, medRxiv Mar 2025. |
| https://pubmed.ncbi.nlm.nih.gov/40673126/ | 200 OK — Thotapalli et al., GPT-4 youth psychiatric emergency triage, PCN Reports 2025. |
| https://arxiv.org/abs/2502.08177 | 200 OK — SycEval (Fanous et al. 2025), Stanford. (Found but not included as a primary entry; medical evaluation is not the central focus.) |
| https://arxiv.org/abs/2602.12285 | 200 OK — "From Biased Chatbots to Biased Agents" (Cao et al. 2026). (Found but not included; persona-bias in agentic systems, not specifically mental health.) |

### Searches that returned no qualifying papers (gap evidence)

- "LLM involuntary commitment Baker Act Kendra's Law evaluation" — no matching LLM eval paper found.
- "LLM mental health Tarasoff third party warning arxiv 2025" — no matching paper found.
- "arxiv involuntary psychiatric LLM legal hold competency 2025" — no matching paper found.
- "LLM forensic psychiatry competency civil commitment evaluation" — only Sciencedirect S016025272500055X (LLMs *extracting* variables from forensic reports, not evaluating LLM forensic decisions).
- "LLM social work child protective services welfare evaluation reporting" — only general AI-in-CPS commentary; no LLM evaluation paper.

### Papers ruled out (initially appeared relevant; on inspection, do not exist or do not match described content)

These were all listed in the prior confabulated review or surfaced during this rebuild and confirmed to be **not real** or **mis-described**:

- Wagner, Hassan, Lee (2025) "Mandated Reporter Scenarios" JAMA Network Open — **does not exist**.
- Levkovich & Elyoseph (2025) JMIR Mental Health on C-SSRS — **does not exist** (real C-SSRS / LLM paper is Patil et al. 2025, arxiv 2505.13480).
- Patel, Browne, Varga (2025) npj Digital Medicine AOT scoping review — **does not exist**.
- Park, Desai, Kumar (2024) "CrisisBench" — **does not exist** (real crisis benchmark is Arnaiz-Rodriguez et al. 2025, arxiv 2509.24857).
- Gupta et al. (2025) "SafetyBench-MH" — **does not exist** (real medical-LLM safety benchmark is CARES, arxiv 2505.11413).
- Chen et al. (2025) "Role-Play Fidelity in LLM-Simulated Psychiatric Patients" — **does not exist** (real LLM-as-psychiatric-patient work is PATIENT-Ψ, arxiv 2405.19660 and PSYCHE, arxiv 2501.01594, neither matching the described "danger-cue sanitization" finding).
- Ramirez et al. (2025) "Forensic Psychiatric Decisions" — **does not exist**.
- Torous, Bhugra, Stein et al. (2025) "Regulatory Evaluation Frameworks Delphi" JMIR Mental Health Oct 2025 — **could not verify**. Not included.
