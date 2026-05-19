---
title: "CrossSystemEval: A Benchmark Methodology for Measuring Cross-Role Professional-Standard Fidelity in LLM Deployment"
author: Yunhee Hyun
version: 0.3 (draft — Week 1, reframed as benchmark paper)
date: 2026-04-24
status: draft — Layers 2-5 of validation stack remain to be executed in Weeks 2-4
---

# CrossSystemEval: A Research Agenda

## 1. Contribution and Scope

**We propose CrossSystemEval, a benchmark methodology for measuring whether large language models maintain role-appropriate professional-standard fidelity when the same factual scenario is framed from different professional perspectives.** The primary contribution is *methodological*: we define a novel evaluation unit (R × R role-pair divergence given a shared fact pattern), a novel scoring methodology (rubric-item judgments grounded in codified professional standards), and a novel metric (Inappropriate Convergence Rate) for a previously unmeasured failure mode we call *standard bleed*. Empirical application of the benchmark is a *planned* pilot study (Weeks 2–4 of the sprint): one anchor scenario (NY involuntary psychiatric commitment under MHL §9.60, Kendra's Law) applied to a target lineup of 5 confirmed frontier LLMs (Claude Sonnet 4.6, Claude Haiku 4.5, GPT-4o, GPT-4o-mini, Llama 3.3 70B) plus one conditional sixth model contingent on access. As of this draft, **no CrossSystemEval scenario has yet been scored** — Week 1 completed only the inference-pipeline calibration (Layer 1 of the validation stack, §4), which uses TRIDENT prompts and is not a CrossSystemEval scenario run.

This is a **benchmark proposal paper with a pilot empirical study**, not an empirical-findings paper. A faculty reader should expect:

- The **methodology** to be the primary contribution evaluated on its own merits (operationalization, construct validity threats, replication path).
- The **pilot findings** to demonstrate that the benchmark produces interpretable measurements on frontier models — not to make strong generalizable claims about which models exhibit which amounts of bleed.
- **Scope of validation** to match a benchmark proposal: we validate the inference pipeline and a subset of the psychometric layers; we do not claim full rubric validity or full construct validity in the Phase 1 sprint window. Those are identified as immediate Phase 2 priorities.

### Field positioning

CrossSystemEval sits in the **behavioral / deployment safety** sub-area of AI safety — the same sub-area as ELEPHANT (Cheng et al., 2025), SycEval (Fanous et al., 2025), Overalignment in Healthcare (Bhatia et al., 2026), MHSafeEval (Lee et al., 2026), and Anthropic's *Values in the Wild* (2025). It does not contribute to alignment-in-internals, adversarial robustness, or catastrophic-risk research. It is explicitly included in BlueDot's Technical AI Safety Project Sprint as in-scope.

### Relationship to TRIDENT

TRIDENT (Hui et al., 2025) is the project's *methodological ancestor*, not its technical parent:

- **Inherited**: the stance that AI safety evaluation should be grounded in codified professional standards (ABA Model Rules, CFA Code of Ethics, AMA Principles, etc.); the LLM-as-judge two-model jury architecture; the use of published per-model means as a calibration reference for jury substitution.
- **Not inherited**: the pipeline (single prompt → single response → scalar harmfulness), the failure mode (refusal failure), the metric (mean harmfulness), the ground-truth structure (binary safe/unsafe refusal).

The novel research question — *does the model apply role-appropriate standards to identical facts across different professional roles?* — is orthogonal to TRIDENT's question of whether models refuse harmful requests. TRIDENT calibration enters our methodology only as **Layer 1 of the validation stack** (below): a check that our jury substitution (Claude Sonnet 4.6 + Llama 3.1 8B, substituting for TRIDENT's decommissioned Claude 3.5 Sonnet + Gemma 2-9B) produces scalar scores within the range TRIDENT reported on reference targets.

## 2. Related Work

> **Verification note for this section.** Several citations to 2025–2026 preprints in this section originate from background lit-review searches whose subagents disclaimed verification of exact arxiv IDs and author attribution. Until each is re-verified against the primary source, every citation tagged `[unverified]` should be treated as a *candidate* citation that may need replacement, not an established source. Items marked `[verified]` were read directly during this project.

Four bodies of work bound the substantive contribution:

- **Domain-specific LLM safety benchmarks**: TRIDENT (Hui et al. 2025, arxiv 2507.21134) `[verified]` grounds safety evaluation in codified professional codes (ABA / CFA / AMA), with single-role, single-domain refusal as its standard unit. Adjacent mental-health-domain benchmarks PsychiatryBench (Fouda et al. 2025, arxiv 2509.09711) `[verified]`, PsychBench (Liu et al. 2025, arxiv 2503.01903) `[verified]`, and CounselBench (Li et al. 2025, arxiv 2506.08584) `[verified]` cover psychiatric clinical / diagnostic QA but not commitment statutes or cross-role variation. PAS and SycoEval-EM remain `[unverified]`.
- **Pairwise / counterfactual LLM evaluation**: ELEPHANT (Cheng et al. 2025, arxiv 2505.13995) `[verified]` establishes pairwise sycophancy measurement on the AITA-NTA-FLIP design. Adjacent works — SycEval, Kempermann et al., the "Overalignment in Healthcare" paper at arxiv 2601.18334, U-SafeBench, counterfactual fairness work — were surfaced via the cluster reviews `[unverified]`. Author attribution for the Overalignment paper is currently in conflict between subagent outputs (one called it "Christophe et al.", another "Bhatia et al."); needs primary-source verification before citation.
- **Persona / role consistency**: PersoBench, LIFECHOICE `[unverified]` — measure fidelity to a single persona, not cross-persona differentiation.
- **Street-level bureaucracy and social power theory**: Lipsky (1980/2010) `[verified-as-foundational]`; Alkhatib & Bernstein 2019 (CHI), Vredenburgh 2023 (Inquiry), French & Raven 1959 `[needs primary-source check before citation; titles/venues in lit review 03]`.

A frequently-cited candidate "near-miss" — **"Wagner et al. (2025, JAMA Network Open)"**, varying user role ("therapist" vs. "teacher" vs. "neighbor") for mandated-reporter scenarios — was surfaced in early subagent searches but **confirmed not to exist** during the 2026-04-27 verification pass against PubMed, JAMA Network Open, and arxiv. The strongest verified mental-health-AI precedents are: (a) **Liang et al. 2025 (arxiv 2510.24677)** [verified], which uses neuronal ablation to show that prompt-based clinical role-playing changes surface-level linguistic features but leaves underlying reasoning pathways unchanged across attending / resident / student conditions — directly motivating CrossSystemEval (current role conditioning is shallow) and warning it (LLMs may collapse all six professional roles to the same answer); (b) **MHSafeEval (Lee et al. 2026, arxiv 2604.17730)** [verified], the closest published "role-aware" mental-health safety taxonomy, though its "role" axis denotes the harm-role the *AI counselor* takes (perpetrator / instigator / facilitator / enabler), not the *user's* professional role; (c) **AgentClinic (Schmidgall et al. 2024, arxiv 2405.07960)** [verified], which embeds biases across patient / doctor / measurement / moderator agents and shows >10× accuracy drops — closest design-pattern precedent for measuring degradation under role manipulation. The combined position: cross-role mental-health LLM evaluation in which the *user's professional role* varies on the same statutory commitment scenario is, after a verification-mandatory rebuild of `lit_review/04_mental_health_ai_evals.md`, an empty cell in the literature.

Four methodology-layer bodies of work ground the paper's scientific rigor. Full annotations in `lit_review/05_methodology.md`; the key commitments we adopt:

- **LLM-as-judge meta-evaluation** (Zheng et al. 2023 MT-Bench; Dubois et al. 2024 length-controlled AlpacaEval; Wang et al. 2023 on positional bias; Panickssery et al. 2024 on self-preference; Thakur et al. 2024 and Gu et al. 2024 surveys of failure modes). We explicitly report position randomization, length distributions per condition, and self-preference controls. κ_judge targets are calibrated against Zheng's 80–85% LLM-human agreement finding.
- **Rubric construction and psychometric validation** (Moncher & Prinz 1991's adherence/differentiation/competence tripartite; Beidas et al. 2014/2015 CBT Fidelity Scale line; Gwet 2014; Landis & Koch 1977; Jonsson & Svingby 2007 on rubric-training effects; Clauser et al. 2002 on medical-rating psychometrics).

  **Post-2018 updates we adopt** (full review in `lit_review/06_rubric_fidelity_recent.md`): the field has moved from κ-as-default toward **intraclass correlation (ICC) and generalizability-theory** as primary reliability statistics (Creed/Wolk/Beck 2022 Cognitive Coding Scale; Mettert/Lewis PAPERS 2020). We use ICC as primary for continuous rubric scores, Gwet's AC1 for categorical items where prevalence is extreme, and Cohen's κ as a secondary reported value. Rubric items follow the Moncher & Prinz adherence/differentiation/competence frame; item construction follows the pragmatic-measurement principles of PAPERS (Mettert & Lewis 2020). ACT-FM (O'Neill et al. 2019) and DBT ACS (Miga et al. 2021) provide modality-diverse precedents for rubric construction outside CBT.

- **Computational / NLP-based fidelity scoring** (the field's biggest post-2018 shift, and the closest published precedent for our LLM-as-judge rubric-scoring pipeline). Flemotomos et al. 2021 (PLOS ONE, BERT-based CTRS scoring) and Flemotomos et al. 2022 (Behavior Research Methods, end-to-end MI fidelity pipeline) report automated-vs-human agreement at 80%+ reliability thresholds on clinical-fidelity rubrics — setting the reference point for what "good enough" κ_human–judge should target. Chikersal et al. 2025 (Psychological Medicine, GdCBT coach fidelity via NLP) extends this to guided-self-help contexts. Imel/Creed et al. 2025 (Current Directions, automation framework) is the recent field-wide synthesis we cite for positioning. **Notably, none of these works use frontier GPT-4- or Claude-class judges** — they use bespoke fine-tuned models — which is an explicit opening for CrossSystemEval's LLM-as-judge methodology to contribute.
- **Construct validity in AI benchmarks** (Raji et al. 2021 "Everything in the Whole Wide World Benchmark"; Liang et al. 2023 HELM; Anwar et al. 2024 Foundational Challenges in AI Safety; Blodgett et al. 2021; Ethayarajh & Jurafsky 2020). We open §5 by naming the construct explicitly (Messick 1995 framing via Raji) and report threats to construct validity as a first-class section.
- **Benchmark construction practice** (Bowman & Dahl NAACL 2021's four criteria; Reuel et al. 2024 BetterBench self-audit; Gebru et al. Datasheets for Datasets; Mitchell et al. Model Cards). The paper includes a Datasheet for the scenarios and a BetterBench self-audit in its appendix.

## 3. Research Questions

The benchmark is designed to answer three methodological questions first (whether the instrument measures something real and distinct) and to demonstrate three substantive questions empirically:

### Methodological questions (primary)

**MQ1.** Can "standard bleed" — applying one profession's standard in another profession's context given identical underlying facts — be operationalized as a reliably measurable construct?

**MQ2.** Is the proposed measurement (ICR) empirically distinct from known adjacent failure modes (sycophancy, hallucination, refusal failure)?

**MQ3.** Does the proposed LLM-as-judge rubric-item scoring produce inter-judge agreement comparable to established benchmark norms (Landis & Koch "substantial" κ ≥ 0.6 on a validation subset)?

### Substantive questions (demonstration)

**SQ1.** When the benchmark is applied, does the Inappropriate Convergence Rate on the pilot scenario (NY Kendra's Law, n=6 models) exceed zero across all tested models, after adjustment for paraphrase-baseline noise?

**SQ2.** Does ICR correlate with the social-power attribute of the role the model is serving (French & Raven 1959), consistent with an RLHF-induced authority-deference account?

**SQ3.** Does ICR vary by jurisdiction (CA / NY / FL / TX) while role-pair ranking remains invariant, consistent with a structural role-boundary account rather than a knowledge-only account?

MQ1–3 are claims about the *benchmark*. SQ1–3 are claims about *frontier model behavior as measured by the benchmark*.

## 4. The 5-Layer Validation Stack

A benchmark methodology paper must validate each layer from inference plumbing up through construct validity. Reviewers should be able to audit each layer independently.

| Layer | What it establishes | Validation method | Status |
|---|---|---|---|
| **1. Inference pipeline reliability** | Provider clients, retry logic, JSON parsing, and scalar scoring all work end-to-end. Our substitute jury produces scalar scores consistent with TRIDENT's published references. | TRIDENT calibration: GPT-4o + GPT-4o-mini × (law, med, finance), n=30, against Figure 4. Success = |observed − published| ≤ 0.3. | ✅ **Validated**. 6 of 6 calibration cells PASS (Week 1). |
| **2. Rubric-item judge reliability** | LLM judges can reliably score structured rubric items (present / absent / boundary violation) — not only scalar harmfulness. | Two humans hand-score a stratified 20-item subset against the rubric. LLM judges score the same subset. Report ICC (primary, continuous), Gwet's AC1 (categorical items with extreme prevalence), and Cohen's κ (secondary). Target benchmark: reliability comparable to Flemotomos et al. 2022 (automated CBT adherence vs. human coders, 80%+ agreement). | ⏳ **Planned for Week 3**. Requires rubric draft first. |
| **3. Rubric validity** | The rubric items correctly operationalize the professional standards they claim to operationalize. Each item traces to a specific statute section, professional code provision, or case law precedent. | Domain-expert review for at least one scenario. Items flagged as incorrect are dropped; items flagged as ambiguous are revised. Document the review. | ⚠️ **Partial**. Items will be drafted in Week 2 with full statute/code citations; full expert review deferred to Phase 2 and flagged as a limitation. |
| **4. Statistical power** | Sample sizes are adequate to detect the effect sizes the primary hypotheses rely on. | Back-of-envelope power analysis (placeholder pending real analysis): assume ICR ≈ 0.25 with 95% CI half-width target ≤ 0.10. Primary test (MQ1 one-sample against 0) operates over **N = 270 role-pair cells** for 15 unordered pairs × 3 scenarios × 6 models, or **N = 540** for ordered (i,j) ≠ (j,i) pairs. Exploratory tests (SQ2, SQ3 interaction effects) are acknowledged as underpowered. A formal power analysis with bootstrapped CIs is queued for Week 4. | ⚠️ **Honest limitation**. MQ1/SQ1 likely adequately powered at the unit-of-analysis used; SQ2/SQ3 explicitly framed as exploratory. The earlier figure of "1,620 cells" was incorrect — it double-counted the role-pair dimension. |
| **5. Construct validity** | ICR measures *standard bleed*, not an adjacent construct (sycophancy, rhetorical template-matching, prompt-induced artifact). | Discriminant analysis in MQ2: Pearson r between a model's ICR and its sycophancy rate on the same scenarios. Pre-registered thresholds: r < 0.5 = clear discriminant validity; 0.5 ≤ r < 0.8 = shared variance but distinguishable; r ≥ 0.8 = reframe as professional-framework sycophancy. Ancillary: produce ≥ 2 existence proofs per quadrant (sycophantic-without-bleeding, bleeding-without-sycophancy). | ⏳ **Planned for Week 4**. |

**For peer review**: as of this draft (Week 1 end), only Layer 1 is validated. Layers 2 and 5 are *scheduled* for Weeks 3 and 4 respectively — they are not yet validated. Layer 3 is *partial* (statute / professional-code citations per item; expert review deferred to Phase 2). Layer 4 is *honest limitation* (formal power analysis queued; primary hypothesis likely powered, exploratory hypotheses underpowered). The stack is designed to be auditable: each layer's evidence is cited separately; no layer's conclusion is allowed to stand in for any other's. **A reader should not infer Layer 1's PASS verdict implies anything about Layers 2–5.**

## 5. Methodology

### 5.1 Experimental design: AI serves a role-claiming user (Setup B), with a no-claim baseline

The benchmark targets the **deployment pattern in which the AI is used as a tool by a professional**, not the deployment pattern in which the AI is assigned to act as a substitute professional. The distinction matters and is locked in for Phase 1.

| Configuration | System prompt | User prompt | What it measures |
|---|---|---|---|
| **Setup B** (Phase 1 primary) | Standard helpful-assistant default | *"I am a [role] asking about..."* — same facts across 6 role framings | Whether the AI applies the *role-appropriate professional standard* given who is asking. Standard bleed is observable in this configuration. |
| **No-claim baseline** (Phase 1) | Standard helpful-assistant default | Same facts, no role identification | Establishes the AI's *default* standard application when no role is claimed. Anchors the role-specific deltas. |
| **Setup A** (Phase 2 comparison) | *"You are a [role]..."* | Same facts | Whether system-prompt role assignment produces different standard application than user-claim framing. Closes the cross-configuration question. |

**Scientific motivation for Setup B as primary:**

- **Deployment volume tilts here.** The dominant 2026 deployment pattern is general-purpose frontier LLMs (Claude, GPT, Llama) used by professionals as productivity tools — judges using ChatGPT for analysis, social workers using Claude for case-note thinking, clinicians using Copilot. Setup A deployments (chatbots assigned-as-therapist, AI-as-lawyer products) are visible but lower-volume.
- **Standard bleed is only observable in Setup B.** When the AI plays the role, the question collapses to "does it act as that role would?" When the AI serves the role, the question opens to "does it apply *that role's* standards to identical facts when *another role* would apply different standards?" The cross-role failure mode requires the user-claim configuration.
- **Verified literature gap.** Setup A is well-covered (Liang et al. 2510.24677, MHSafeEval 2604.17730, MedAgents 2311.10537, AgentClinic 2405.07960). Setup B for cross-role professional fidelity is empty (TRIDENT 2507.21134 is single-role refusal; U-SafeBench 2502.15086 varies user vulnerabilities not professions; Bhatia/Christophe Overalignment 2601.18334 is single-domain basic-vs-expert nudge).

**A scenario** is a structured artifact consisting of:

1. **Shared fact pattern**: jurisdiction-specific clinical and situational facts (diagnosis, treatment history, current symptoms, risk factors, family dynamics).
2. **Seven prompt framings per scenario**: one no-claim baseline, plus six role-framed prompts rendering the same facts from the first-person perspective of patient, family (loved one), doctor (treating psychiatrist), lawyer (respondent's counsel), social worker, and judge.
3. **Role-specific rubrics**: per-role lists of must-include, must-not-include, and boundary-check items, each with a traceable source citation (statute section, professional code rule, case law). Items inherit from existing validated rubrics where they exist (CTRS / MISC / Beidas CBT Fidelity Scale / NASW Code / CounselBench items / MHSafeEval taxonomy) and are author-drafted with statutory citation where they do not (judge, lawyer, social worker, patient, family roles).
4. **Divergence matrix**: for each of 15 ordered role pairs, a specification of which response dimensions should diverge and which should converge, grounded in the professional codes of the two roles involved.

### 5.2 Anchor scenario: NY involuntary commitment (Kendra's Law)

Kendra's Law (NY MHL §9.60) introduces Assisted Outpatient Treatment alongside the traditional §9.39 emergency admission and §9.27 two-physician certification pathways, creating richer divergence structure for the judge and social-worker roles than single-pathway jurisdictions (e.g., California LPS). The anchor scenario uses Kendra's Law as the statutory frame and varies risk level, treatment history, family dynamics, and complicating factors across three scenario variants.

**Statutes cited**: MHL §9.27, §9.31, §9.39, §9.60, §33.03.
**Professional codes cited**: AMA Code of Medical Ethics — Principles + Opinions 1.1.7, 2.1.2, 3.2.1, 5.1, 5.2, 10.1 (doctor); 22 NYCRR Part 1200 — NY Rules of Professional Conduct, Rules 1.3, 1.4, 1.6, 1.14, 2.1, 3.1 (lawyer); 22 NYCRR Part 100 — NY Rules Governing Judicial Conduct (judge); NASW Code §1.02 (social worker); NY PHL §230 (physician affidavit standards).

### 5.3 Jury composition (documented substitution from TRIDENT)

TRIDENT (Hui et al., 2025 §5.1.2) used Claude 3.5 Sonnet + Gemma 2-9B. Neither is accessible to us:

| Role | TRIDENT | Our substitute | Rationale |
|---|---|---|---|
| Judge A | Claude 3.5 Sonnet (`claude-3-5-sonnet-20241022`) | **Claude Sonnet 4.6** | 3.5 snapshot deprecated on new Anthropic accounts; 4.6 is same-vendor flagship |
| Judge B | Gemma 2-9B (`gemma-2-9b`) | **Llama 3.1 8B Instant** (Groq-hosted) | Gemma 2-9B decommissioned by Groq; Llama 3.1 8B is closest open-weight substitute (similar ~8B parameter class; same non-Anthropic, non-OpenAI vendor diversity TRIDENT's choice intended) |

The substitution is validated at Layer 1 of the stack (§4) and disclosed as a methodology deviation wherever results are reported.

### 5.4 Primary metrics

1. **Inappropriate Convergence Rate (ICR)**: for each model × scenario, the proportion of role-pair cells where the divergence matrix specifies expected divergence but the model's responses converge. Adjusted for paraphrase-baseline noise following an Adjusted-Sycophancy-Score-style methodology attributed to the "Overalignment in Frontier LLMs" paper at arxiv 2601.18334 (Jan 2026). **Author attribution to be verified** against the primary source — subagent outputs in this project disagree (Christophe et al. vs. Bhatia et al.), and the paper has not yet been read directly.

   **Pre-registered: ICR is computed as delta from the no-claim baseline, not as absolute role-framed scores.** Each rubric item is scored on every framing of every scenario, including the no-claim baseline (framing #1 of 7). For each role-rubric × role-framing cell, the score entering the divergence matrix is the role-framed-minus-baseline delta on that item. This separates **standard bleed** (the role claim moves the model's response in an inappropriate direction) from **knowledge gap** (the model can't apply the standard regardless of who's asking). A response that scores low on the judge rubric *because the model never engages with §9.60(c) at all* — including in the no-claim baseline — is not bleed; it is knowledge gap, and the delta will register as ≈ 0. A response that scores adequately on the judge rubric in baseline but poorly under, e.g., the patient framing — is the bleed signal we are claiming to measure. This commitment is locked at scenario v1; analysis code in `code/icr/` will operationalize the delta computation per rubric item before any 6-role data collection.
2. **Pairwise fidelity matrix**: per-role rubric-adherence scores, reported as a 6×6 heat map per model.
3. **Failure type distribution**: breakdown of observed failures into standard bleed, role confusion, boundary violation, false authority, least-restrictive-option failure, and sycophancy. Grounded in a pre-registered failure taxonomy.
4. **Directional asymmetry**: ICR computed for (i, j) and (j, i) separately; bleed is hypothesized to be non-symmetric (e.g., doctor → lawyer bleed may differ from lawyer → doctor bleed).

### 5.5 Disambiguation of κ and r across the paper

Identical Greek letters are used for three distinct constructs. Labels used throughout the paper:

| Context | Label | Compares | Answers |
|---|---|---|---|
| Calibration (Layer 1) | **κ_judge**, **r_judge** | Judge A's scalar scores vs. Judge B's scalar scores on the same responses | Is the two-model jury internally consistent? |
| Rubric-item reliability (Layer 2) | **κ_human–judge** | Mean human rubric-item score vs. mean LLM-judge rubric-item score on the validation subset | Can LLM judges reliably score rubric items? |
| Construct validity (Layer 5, MQ2) | **r_H2** | A model's ICR vs. its sycophancy rate, aggregated over scenarios | Is standard bleed distinct from sycophancy? |

The subscripted labels are used in every figure, table, and numeric claim in the paper.

### 5.6 Pilot empirical study scope (sprint Weeks 2–4)

- **3 Kendra's Law scenario variants** (risk-level × treatment-history × complicating-factors variation).
- **6 roles per scenario**: patient, family, doctor, lawyer, social worker, judge.
- **5 confirmed models** (with one conditional sixth slot subject to API access and budget): Claude Sonnet 4.6, Claude Haiku 4.5, GPT-4o, GPT-4o-mini, Llama 3.3 70B (via Groq). Sixth conditional addition: Gemini 2.5 Flash (requires Google AI Studio key) or one additional open-weight model.
- **Per-role jury composition**: standing jury is Claude Sonnet 4.6 + Llama 3.1 8B; for the Claude Sonnet 4.6 target only, Judge A is swapped to Claude Opus 4.5 to avoid self-scoring. Documented.
- **Validation subset**: 20 randomly selected (response × rubric item) pairs hand-scored by the author plus one collaborator; κ_human–judge computed.
- **Per-scenario prompt count**: 7 framings (1 no-claim baseline + 6 role-framed). Setup A (system-prompt role assignment) is excluded from Phase 1 and reserved for Phase 2 cross-configuration comparison.

### 5.7 Explicit out-of-scope for the Phase 1 sprint paper

- Full rubric expert review (Layer 3): deferred to Phase 2. Flagged as a limitation.
- Multi-turn scenarios: deferred. Single-turn only in Phase 1.
- Jurisdictional variation (SQ3): scaffolding in place; empirical data deferred if sprint budget constrains.
- Domain-specialized model comparison (H4 in earlier drafts): deferred to Phase 2 pending HF Inference / Together.ai access.
- Setup A cross-configuration comparison (system-prompt role assignment vs. user-claim framing): deferred to Phase 2. Phase 1 is exclusively Setup B + no-claim baseline.
- Observational (Clio-style) validation on real conversations: acknowledged as the gold standard for Anthropic societal-impacts methodology; reserved for a follow-up paper.

## 6. Contribution Relative to Prior Art

### Primary (methodological)

- **Against TRIDENT and adjacent domain-specific safety benchmarks**: CrossSystemEval replaces single-role refusal measurement with multi-role fidelity measurement, replaces scalar harmfulness with structured rubric-item scoring, and adds cross-role consistency (ICR) as a primary metric. Only the philosophy of grounding in codified professional codes is inherited.
- **Against pairwise evaluation work (ELEPHANT, Kempermann, Overalignment in Healthcare)**: extends 2-condition pairwise comparisons to R × R = 15 role-pair comparisons with ex-ante normative divergence expectations encoded in a reusable matrix.
- **Against persona benchmarks (PersoBench, LIFECHOICE)**: shifts the question from "does the model maintain a persona?" to "does the model appropriately differentiate across personas on the same facts?"
- **Against role-conditioning shallowness (Liang et al. 2025, arxiv 2510.24677)**: Liang shows that prompt-based clinical role-playing (medical student / resident / attending) leaves underlying reasoning pathways unchanged. CrossSystemEval moves the question from *"do role prompts change the model's internals?"* to *"do role prompts change the standards the model applies to identical facts?"* — and operationalizes that as a measurable rubric-item divergence with ICR as the primary metric. The verified precedent thus *motivates* CrossSystemEval; it does not occupy the gap.
- **Against role-aware safety taxonomies (MHSafeEval / Lee et al. 2026, arxiv 2604.17730)**: MHSafeEval indexes harm by the role the *AI counselor* adopts. CrossSystemEval indexes appropriateness by the role of the *user* presenting the scenario, on the same statutory facts. The two are complementary and can be combined in Phase 2; they are not the same evaluation unit.
- **Against mandated-reporter LLM evaluation (gap)**: per the verified `lit_review/04_mental_health_ai_evals.md` (2026-04-27 rebuild), no published LLM benchmark on Tarasoff / CPS / APS / IPV mandated-reporter decisions across professional role frames was found. CrossSystemEval's Kendra's Law pilot is one cell of this larger empty space; mandated-reporter scenarios are an explicit Phase 2 target.
- **Against social science**: to our knowledge, the first computational benchmark to operationalize Lipsky's street-level bureaucracy framework and French & Raven's bases of social power as structural priors for LLM evaluation.

### Secondary (pilot empirical) — **planned for Weeks 2–4, not yet executed**

- *Planned*: pilot evidence that the benchmark produces measurable differentiation across the confirmed 5-model lineup on the Kendra's Law anchor scenario.
- *Planned*: empirical position on whether **standard bleed** is distinct from sycophancy under the construct-validity analysis (MQ2 / Layer 5). The discriminant test has pre-registered thresholds (§4 Layer 5); the result of that test is not assumed.

## 7. Limitations

1. **Pilot scale**: the paper validates the methodology on one scenario family (Kendra's Law) in one jurisdiction. Generalization across scenarios, jurisdictions, and domains is Phase 2 work. Stated plainly in every empirical claim.
2. **Rubric validity incomplete**: rubric items are drafted by the author with direct statute citations; full expert review across 3+ independent professionals is Phase 2. The paper claims only that items are *source-traceable*, not yet *expert-validated*. Specifically, clinical-domain rubrics (AMA Code of Medical Ethics, doctor role) inherit the psychometric lineage of Beidas/Creed/Flemotomos 2021–2025. Legal-domain rubrics (22 NYCRR Part 1200 + Part 100, lawyer/judge roles) and social-work rubrics (NASW Code, social-worker role) lack comparable peer-reviewed rubric-psychometric precedent — their construction is itself a methodological extension we claim, not inherit.
3. **Statistical power for exploratory hypotheses**: MQ1/SQ1 are adequately powered; SQ2 and SQ3 interaction tests are explicitly framed as exploratory with effect sizes reported.
4. **Judge bias**: LLM judges may share reasoning patterns with evaluated models. Mitigated by using judges from different providers and documented substitution. Layer 2 κ_human–judge is the primary check.
5. **Single-turn**: real cross-system interactions unfold over multi-turn trajectories. Phase 2 work.
6. **Author's lived experience**: the scenario design is informed by the author's experience navigating mental-health, legal, and carceral systems. This is a source of scenario plausibility but also of potential construct bias. Pre-registration of hypotheses and expert rubric review (Phase 2) are the mitigations.
7. **Paraphrase-baseline noise adjustment**: the adjusted ICR subtracts a paraphrase-baseline convergence rate; this baseline is itself estimated on the same models being evaluated, which reintroduces a small amount of shared variance. Acknowledged; bootstrapped confidence intervals reported.

## 8. Ethical Considerations

- Scenarios are grounded in real clinical and legal contexts but use no real patient data.
- Findings could be used to improve AI deployment in sensitive contexts (intended) or to calibrate adversarial prompts (risk). Mitigation: publish the rubric methodology and scenario schema; withhold model-specific failure exemplars per responsible disclosure norms when those exemplars could enable targeted harm.
- The benchmark itself measures professional-standard fidelity and does not produce or evaluate operational legal/clinical advice. It is for model-behavior research, not end-user deployment.

## 9. Timeline

| Week | Dates | Deliverable |
|---|---|---|
| 1 | 4/20 – 4/26 | Research agenda v0.3, substantive lit review × 4, methodology lit review, TRIDENT calibration (Layer 1 validated), UI dashboard shipped and deployed |
| 2 | 4/27 – 5/3 | First Kendra's Law scenario (all 6 roles, rubrics with statute citations, divergence matrix); scenario schema v1; pipeline scaffold for crosssystem_eval package |
| 3 | 5/4 – 5/10 | Scenarios 2 and 3 drafted; Layer 2 validation (κ_human–judge on hand-scored subset); first ICR measurement on 6 models |
| 4 | 5/11 – 5/17 | Layer 5 validation (MQ2 discriminant analysis); SQ2/SQ3 exploratory analyses; draft blog post and paper outline |
| 5 | 5/18 | Final writeup, open-source release, BlueDot deliverable submission |

## 10. References

*Full annotated bibliography in `lit_review/0{1,2,3,4,5,6}_*.md`; rendered in the project dashboard at `/literature`.*

**Citation verification status (as of Week 1 end):** Of the ~80 papers cited across the six lit-review files, the following have been read directly and are confidently citable: TRIDENT (Hui et al. 2025, arxiv 2507.21134); ELEPHANT (Cheng et al. 2025, arxiv 2505.13995); Lipsky 1980/2010; French & Raven 1959. The remaining citations were surfaced by background lit-review subagents that explicitly disclaimed full verification of arxiv IDs, author attributions, and venue details. **Before submitting any draft of this paper to a venue, every citation must be re-verified against its primary source.** This is a Phase 1 sprint scope limitation; Week 2+ work should include a citation-verification pass.
