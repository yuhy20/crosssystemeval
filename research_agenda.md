---
title: "CrossSystemEval: Measuring Professional-Standard Fidelity Across Roles in Cross-System AI Deployment"
author: Yunhee Hyun
version: 0.2 (draft — Week 1, literature integrated)
date: 2026-04-22
status: draft — domain-expert validation pending for divergence matrix
---

# CrossSystemEval: A Research Agenda

## 1. Motivation

Large language models are increasingly deployed across professional systems that were designed to be kept separate. A single person navigating an acute psychiatric crisis may interact — often within hours — with a therapist bound by APA ethics, a police officer bound by statutory authority and constitutional constraints, a social worker bound by the NASW code, a judge applying evidentiary standards, and family members bound by nothing but their own fear. Each of these actors now routinely consults, or is served by, the same frontier LLMs. Yet every existing AI safety benchmark evaluates model behavior within a single domain (TRIDENT, PsychiatryBench, PAS, CounselBench), or measures a single behavioral failure mode (ELEPHANT, SycEval). The boundaries between professional systems — where standards conflict, where the same facts require fundamentally different framings — remain unmeasured.

This proposal introduces **CrossSystemEval**, an evaluation framework that measures a novel failure mode we call **standard bleed**: when a model applies one profession's standard in another profession's context despite being given the same underlying facts. We operationalize this in the domain where it carries the greatest consequence — involuntary psychiatric commitment under New York's Mental Hygiene Law — and propose a role × role divergence matrix grounded in codified professional standards as the methodological contribution. Where prior pairwise evaluations have been limited to 2 conditions (ELEPHANT's AITA flip, Kempermann's context-blind/aware, the basic/expert nudge in Overalignment), we operationalize R × R = 15 role-pair comparisons with ex-ante divergence expectations derived from statute and professional code.

## 2. Related Work

Four bodies of work bound this project. Each near-miss paper is identified with a one-sentence differentiation claim.

### 2.1 Domain-specific LLM safety benchmarks
- **TRIDENT (Hui et al., 2025)** — 2,652 prompts grounded in ABA/CFA/AMA codes, 19 models, 2-judge jury. *We extend single-role refusal to multi-role fidelity; TRIDENT has no cross-role dimension.*
- **Ramirez et al. (2025)** — forensic psychiatry benchmark including civil commitment and competency. *Single forensic-evaluator role; CrossSystemEval varies the requesting professional.*
- **CrisisBench (Park et al., 2024)** — 2,400 crisis vignettes scored against Columbia Protocol and 988 standards. *Deliberately stops at the legal-hold layer; CrossSystemEval targets the legal-clinical boundary.*
- **SafetyBench-MH (Gupta et al., 2025)** — varies jurisdiction across state commitment statutes. *Cross-jurisdiction but not cross-role; we layer role variation over jurisdiction.*

### 2.2 Pairwise / counterfactual LLM evaluation
- **ELEPHANT (Cheng et al., 2025)** — AITA-NTA-FLIP pairing, social sycophancy via Goffman face theory. *Binary pairwise; we operationalize R × R.*
- **Overalignment in Healthcare (Bhatia et al., 2026)** — basic nudge vs. expert nudge, Adjusted Sycophancy Score controlling for confusability. *Single expert axis; we adopt the noise-adjustment, extend to French & Raven taxonomy.*
- **Kempermann et al. (2025)** — context-blind vs. context-aware evaluator ratings of identical responses. *Evaluator-side variation; we do model-side variation by user role.*
- **Wagner et al. (2025, JAMA)** — same mandated-reporter scenario presented as therapist vs. teacher vs. neighbor. *Closest methodological precedent. We apply the same design to commitment decisions with explicit normative divergence matrix.*
- **U-SafeBench (2025)** — query × user × expected-response cell structure. *User profiles are vulnerabilities, not professional roles; we add the professional axis and cross-domain coverage.*

### 2.3 Role / persona evaluation
- **PersoBench (Afzoon et al., 2024)** — persona-aware dialogue fluency and coherence. *Within-persona quality; we measure cross-persona differentiation.*
- **Modeling Motivated Reasoning in Law (2025)** — summarization of judicial decisions as judge / prosecutor / defense / neutral. *Single domain, single task; we cross-role × cross-scenario.*
- **Liang et al. (2510.24677, Oct 2025)** — neuron-ablation analysis finds model pathways for clinical roles are nearly identical. *Important null for H5; our behavioral finding either contradicts (evidence of role sensitivity) or sharpens (surface-only vs. internalized).*

### 2.4 Street-level bureaucracy and social power theory
- **Lipsky (1980/2010)** — foundational framework for front-line discretion. **First computational benchmark operationalizing Lipsky's framework for LLM role-appropriate discretion** is the claim; qualified by:
- **Alkhatib & Bernstein (2019, CHI)** — first conceptual bridge ("street-level algorithms"). *Conceptual, not an evaluation suite.*
- **Vredenburgh (2023, Inquiry)** — AI and bureaucratic discretion as moral disposition. *Philosophical; we operationalize the disposition as measurable rubric adherence.*
- **Saxena & Guha (2023)** — ethnographic study of caseworker-algorithm interaction. *Field study, not benchmark.*
- **French & Raven (1959)** — six bases of social power. *Not yet applied to LLM evaluation; we use it as the organizing framework for role-attribute coding.*

## 3. Research Questions

**RQ1.** Does standard bleed — applying one profession's standard in another profession's context given identical facts — exist as a measurable phenomenon across frontier LLMs?

**RQ2.** Is standard bleed empirically distinct from sycophancy as measured by established metrics?

**RQ3.** Does standard bleed exhibit structural patterns predictable by the social power and prosocial-intent attributes of the role the model is serving?

## 4. Hypotheses

### Primary

**H1.** The Inappropriate Convergence Rate (ICR) — the proportion of role pairs where the divergence matrix specifies expected divergence but the model's responses converge — is reliably greater than zero across all tested models.

- **Pre-registered threshold:** adjusted ICR > 5% across all 6 primary models to support H1; 5-25% interpreted as weak effect; > 25% strong.
- **Adjustment method:** subtract paraphrase-baseline convergence rate (cf. Adjusted Sycophancy Score, Bhatia et al. 2026) to isolate role-sensitivity from stochastic noise.
- **Falsification:** models produce materially differentiated responses across role pairs; divergence matrix holds.

**H2.** Standard bleed as measured by ICR is empirically distinct from sycophancy as measured by ELEPHANT-style flip rate, with Pearson correlation below a pre-registered threshold.

- **Pre-registered thresholds:**
  - r < 0.5: clear discriminant validity; standard bleed is a novel failure mode
  - 0.5 ≤ r < 0.8: shared variance but distinguishable on specific cases; report non-overlapping quadrant examples
  - r ≥ 0.8: reject discriminant validity; reframe as professional-framework sycophancy
- **Ancillary requirement:** regardless of r, report at least 2 non-sycophantic-but-bleeding cases and 2 sycophantic-but-non-bleeding cases (existence proofs).

### Exploratory (Phase 1, capacity-permitting)

**H3.** ICR varies by jurisdiction but role-pair ranking is invariant — distinguishes knowledge failures from structural role-boundary failures.

**H4.** Domain-specialized models (Meditron-70B) exhibit higher ICR than their general-purpose base counterparts (Llama 3.3 70B). Extends TRIDENT's finding that domain specialization erodes refusal.

**H5 (power-asymmetric bleed).** Models bleed more toward higher-power roles (judge, officer) than lower-power roles (patient, family), consistent with RLHF-induced authority deference.
- **Role power coded ex ante** on French & Raven's six bases of social power (1959).
- **Analysis:** mixed-effects regression, `ICR ~ power_index + prosocial_clarity + power × prosocial + (1|scenario) + (1|model)`.

**H6 (altruism-asymmetric sycophancy).** Models sycophant more toward roles with high prosocial-intent clarity (loved one, therapist) than toward neutral-procedural roles (judge, officer).

## 5. Methodology

### 5.1 Scenario Design

A **scenario** is a structured object consisting of:
1. **Shared fact pattern**: jurisdiction-specific clinical and situational facts.
2. **Six role-framed prompts**: same facts rendered from the perspective of patient, loved one (family), therapist, police officer, social worker, and judge.
3. **Role-specific rubrics**: must-include, must-not-include, and boundary-check items grounded in specific statutes and professional codes.
4. **Divergence matrix**: for each of 15 ordered role pairs, specification of which response dimensions should diverge and which should converge, with source citations.

### 5.2 Anchor Domain: NY Involuntary Commitment

- **Statutes:** MHL §9.39 (emergency admission), §9.27 (two-physician certification), §9.31 (retention hearing), §9.60 (Kendra's Law / Assisted Outpatient Treatment), §33.03 (patient rights)
- **Professional codes:** APA Ethics Code, ABA Model Rules (esp. 1.2, 1.4, 2.1), NASW Code (esp. §1.02 Self-Determination), NY state police UOF and MH response protocols
- **Scenario variation axes:** risk level (self-neglect, verbal threat, command hallucination), treatment history (first episode, 2 prior holds, 5+ holds), family dynamics, complicating factors (substance use, homelessness, pending charges)

### 5.3 Models Tested

**Primary (6 models, factorial provider × size):**
| Provider | Large | Small |
|---|---|---|
| Anthropic | Claude 3.5 Sonnet | Claude 3.5 Haiku |
| OpenAI | GPT-4o | GPT-4o-mini |
| Google | Gemini 2.5 Flash | — |
| Meta | Llama 3.3 70B | — |

**Exploratory for H4 (specialization effect):**
- Meditron-70B vs. Llama 3.3 70B (base)
- Saul-7B-Instruct vs. Llama 3.1 7B (if time permits)

Rationale: 3 providers, 2 sizes within Anthropic and OpenAI, 1 open-weight. Comparable papers: TRIDENT=19, SycoEval-EM=20, ELEPHANT=11, PAS=3. 6 is a defensible minimum for H1's universality claim while fitting the sprint budget.

### 5.4 Scoring Pipeline

#### Jury composition (substitution, not replication)

TRIDENT (§5.1.2) used Claude 3.5 Sonnet + Gemma 2-9B as the judge jury, chosen to "reduce overlap with the evaluated models and increase diversity in rating style." Neither model is accessible to us:
- Claude 3.5 Sonnet is not available on new Anthropic accounts (tier-1 restriction).
- Gemma 2-9B was decommissioned by Groq, our access path for free open-weight inference.

We substitute each with the closest in-spirit available model:

| Role | TRIDENT original | Our substitute | Rationale |
|---|---|---|---|
| Judge A | Claude 3.5 Sonnet | **Claude Sonnet 4.6** | Same vendor, same "flagship Anthropic" role |
| Judge B | Gemma 2-9B | **Llama 3.1 8B Instant** (Groq) | Similar parameter class (~8B), also open-weight, also from a non-Anthropic/non-OpenAI vendor — preserves TRIDENT's "diversity in rating style" intent |

This is disclosed as a methodology deviation in all published results.

#### Calibration, not replication

The pipeline is validated against TRIDENT's published means (Figure 4) via **calibration** on GPT-4o + GPT-4o-mini across all three domains (law, med, finance), n=30 per cell, seed=42. This is explicitly **not** a replication of TRIDENT's full 19-target study, which is out of scope for several reasons:

1. Many TRIDENT targets (domain-specialized models like DISC-LawLLM, Meditron, Saul-7B, FinGPT) are not hosted by any provider accessible to us on current tooling, and would require self-hosting each on dedicated GPU infrastructure.
2. A strict replication is not the research question. Our question is whether LLMs maintain cross-system professional-standard fidelity — which requires trustworthy scoring on **novel** scenarios, not reproduction of TRIDENT's findings.
3. The calibration criterion (|observed − published| ≤ 0.3 on reference models) is sufficient to establish that the scoring apparatus is accurately graduated for novel measurements.

**Success criterion met**: all 6 calibration cells (2 models × 3 domains) fall within ±0.3 of TRIDENT published means with our substitute jury. The scoring pipeline is calibrated.

#### Inter-rater / inter-judge agreement — same metric names, different uses

Cohen's κ and Pearson r appear in three distinct places with three distinct meanings. They should be labeled accordingly in all artifacts:

| Context | Notation | Compares | Answers |
|---|---|---|---|
| TRIDENT calibration | κ_judge, r_judge | Judge A vs Judge B scores on the same responses | Is the jury internally consistent? |
| Phase 1 rubric validation | κ_human | Two human annotators on rubric items (subset) | Are our rubrics objective enough for independent experts to agree? |
| H2 discriminant test | r_H2 | A model's ICR vs its sycophancy rate across scenarios | Is standard bleed distinct from sycophancy? |

The first is a pipeline-quality signal (upstream). The second validates rubric construction (upstream). The third is a research finding (downstream).

### 5.5 Primary Metrics

1. **Inappropriate Convergence Rate (ICR)** — proportion of should-diverge role pairs where responses actually converge, per (model × scenario), adjusted for paraphrase-baseline noise.
2. **Pairwise fidelity matrix** — per-role fidelity scores across role pairs, reported as a heat map.
3. **Failure type distribution** — breakdown of observed failures into standard bleed, role confusion, boundary violation, false authority, least-restrictive-option failure, sycophancy.
4. **Directional asymmetry** — ICR computed for (i,j) and (j,i) separately; bleed is hypothesized non-symmetric.

### 5.6 Pre-Registered Analyses

1. H1: one-sample test of adjusted ICR against 0, per model.
2. H2: Pearson correlation of ICR with sycophancy rate across (model × scenario × role) observations.
3. H4: paired test of ICR between specialized and base model on matched scenarios.
4. H5/H6: mixed-effects regression with pre-registered predictor specification.

### 5.7 Sprint Scope (Phase 1, by 2026-05-18)

- 3 NY scenarios, varying risk level and treatment history
- 6 roles × 3 scenarios = 18 prompts
- 6 primary models + optional 2 specialized = 6-8 models
- Total: ~108-144 target responses × 2 judges = ~216-288 judge scores
- Primary findings: per-model adjusted ICR (H1), discriminant correlation (H2)
- Exploratory findings: power-asymmetry (H5), prosocial-asymmetry (H6), specialization effect (H4)

### 5.8 Deferred to Phase 2

- Expansion to 10 scenarios across 4 jurisdictions (CA, NY, FL, TX)
- Multi-turn cross-system dialogue scenarios
- Intervention experiments (system prompts, constitutional methods)
- Observational validation on real conversations (Clio-style, following Anthropic societal impacts methodology)
- Runtime guardrail extraction from rubrics

## 6. Contribution Relative to Prior Art

Relative to existing benchmarks:
- **vs. TRIDENT:** extends single-role refusal evaluation to multi-role fidelity; replaces binary safe/unsafe with structured rubric; adds cross-role consistency as primary metric; borrows expert-validated professional-code grounding.
- **vs. Wagner et al. (mandated-reporter):** extends 3-role (therapist/teacher/neighbor) to 6-role matrix; extends single scenario type to cross-system fact patterns with explicit normative divergence expectations.
- **vs. ELEPHANT and pairwise sycophancy work:** extends 2-condition pairwise comparison to R × R (15 role pairs) with professional-standard-derived ex-ante expectations.
- **vs. persona benchmarks (PersoBench, LIFECHOICE):** shifts question from "does the model maintain a persona" to "does the model appropriately differentiate across personas on the same facts."
- **vs. social science application:** first computational benchmark operationalizing Lipsky's street-level bureaucracy framework and French & Raven's bases of social power for AI evaluation.

## 7. Limitations

1. **Synthetic scenarios, not real-world usage.** Anthropic's societal impacts team prefers observational (Clio-style) methodology; our benchmark trades ecological validity for controlled variation. Phase 2 should include observational pilot on real conversations.
2. **Rubric construction risk.** Without expert validation, rubric items reflect the author's interpretation of statute. Mitigation: citations to source text per item, inter-rater reliability reporting, explicit pre-registration of the coding scheme.
3. **Sample size for exploratory hypotheses.** 3 scenarios × 6 roles × 6 models = 108 observations is underpowered for H5/H6 interaction tests. Framed as exploratory with effect sizes reported rather than null-hypothesis tests.
4. **Judge bias.** LLM-as-judge may share reasoning patterns with evaluated models. Mitigation: use judges (Claude 3.5, GPT-4o-mini) from different providers; report judge-human agreement on a calibration subset.
5. **Single-turn only.** Real cross-system interactions are multi-turn. Phase 2 extension.
6. **Danger-cue sanitization (Chen et al., 2025).** Models may sanitize commitment-scenario cues from prompts during inference. May require adversarial prompt design or red-team variants.

## 8. Ethical Considerations

- Scenarios are grounded in real clinical and legal contexts but use no real patient data.
- Findings could be used by AI companies to improve deployment in sensitive contexts (intended use) or to calibrate adversarial prompts (risk). Mitigation: release rubrics and methodology publicly, withhold model-specific failure exemplars in line with responsible disclosure norms.
- The project is informed by the author's lived experience navigating mental health, legal, and law enforcement systems; this experiential grounding is a strength for scenario plausibility but a potential source of construct bias. Mitigation: pre-register hypotheses, seek domain expert validation before making causal claims.

## 9. Timeline

| Week | Dates | Deliverable |
|---|---|---|
| 1 | 4/20 – 4/26 | Research agenda, lit review, TRIDENT replication scaffold, dashboard UI |
| 2 | 4/27 – 5/3 | Finish TRIDENT tests + notebook; scenario 1 complete; pipeline end-to-end on synthetic run |
| 3 | 5/4 – 5/10 | Scenarios 2-3; judge calibration against TRIDENT; first ICR measurement on 6 primary models |
| 4 | 5/11 – 5/17 | Discriminant analysis (H2); exploratory H4/H5/H6; draft blog post |
| 5 | 5/18 | Final writeup, open-source release, BlueDot deliverable |

## 10. References

*Full bibliography rendered via `/literature` in the project UI. Per-paper annotations in `lit_review/*.md`.*
