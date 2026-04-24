---
slug: methodology
title: "Evaluation Methodology Scaffolding for a Benchmark Paper"
subtitle: "LLM-as-judge validation, rubric psychometrics, construct validity, and benchmark construction"
papers: 21
status: synthesized
date: 2026-04-24
---

## Summary

This review shifts from substantive motivation (Reviews 01–04) to **methodological scaffolding**. A benchmark paper with a new rubric-based pipeline must survive four reviewer objections: (1) *"LLM judges are unreliable"* (Cluster 1), (2) *"your rubric items are arbitrary"* (Cluster 2), (3) *"you haven't shown the benchmark measures what you claim"* (Cluster 3), (4) *"this is a prompt list, not a benchmark"* (Cluster 4). Each cluster maps to the canonical citations that forestall those objections.

**Strongest defensible framing:** construct-validity-first benchmark construction with dual human + LLM-judge scoring, psychometric rubric validation grounded in clinical-fidelity tradition, and explicit treatment of LLM-judge failure modes (position, verbosity, self-preference).

---

## CLUSTER 1 — LLM-as-judge validation methodology

### 1. Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena"
- **Link:** [arxiv 2306.05685](https://arxiv.org/abs/2306.05685) (Jun 2023, NeurIPS 2023 D&B)
- **Contribution:** Foundational empirical result that GPT-4 judges reach ~80–85% agreement with humans, matching human-human agreement. Characterizes position, verbosity, and self-enhancement bias.
- **Cite for:** Primary justification for LLM-as-judge methodology, and the bias list we must report controlling for.

### 2. Dubois et al., "Length-Controlled AlpacaEval"
- **Link:** [arxiv 2404.04475](https://arxiv.org/abs/2404.04475) (Apr 2024)
- **Contribution:** Shows length is the largest confound in LLM-judge scoring; causal-inference correction yields 0.98 Chatbot Arena correlation. Extends Li et al. 2023 (arxiv 2305.14387).
- **Cite for:** Calibration — we must report response-length distributions per role condition and either length-control or argue null effect.

### 3. Wang et al., "Large Language Models are not Fair Evaluators"
- **Link:** [arxiv 2305.17926](https://arxiv.org/abs/2305.17926) (May 2023, ACL 2024)
- **Contribution:** Positional bias — swapping candidate order flips up to ~30% of GPT-4 judgments. Proposes Balanced Position Calibration.
- **Cite for:** Why we randomize item order and, for pairwise comparisons, run both orderings and report only consistent verdicts.

### 4. Gu et al., "A Survey on LLM-as-a-Judge"
- **Link:** [arxiv 2411.15594](https://arxiv.org/abs/2411.15594) (Nov 2024)
- **Contribution:** Taxonomy of judge designs (pointwise/pairwise/listwise) and bias catalog (position, verbosity, self-preference, authority, sentiment, concreteness). See also Li et al. "From Generation to Judgment" (arxiv 2411.16594).
- **Cite for:** Single-citation anchor for the full bias taxonomy in threats-to-validity.

### 5. Thakur et al., "Judging the Judges"
- **Link:** [arxiv 2406.12624](https://arxiv.org/abs/2406.12624) (Jun 2024)
- **Contribution:** Stress-tests 9 judge models; shows κ (not raw % agreement) is the correct reliability metric and that small judges over-agree at the percent level while κ exposes chance-agreement inflation.
- **Cite for:** Why our headline reliability number is κ/AC1, not raw agreement.

### 6. Panickssery et al., "LLM Evaluators Recognize and Favor Their Own Generations"
- **Link:** [arxiv 2404.13076](https://arxiv.org/abs/2404.13076) (Apr 2024)
- **Contribution:** Self-preference bias — GPT-4 rates its own outputs 10%+ higher than equivalent outputs from other models and can self-identify them.
- **Cite for:** Why judge ≠ evaluated model and why cross-judge robustness (Claude judges GPT, vice versa) is required.

---

## CLUSTER 2 — Rubric construction & psychometric validation

### 7. Moncher & Prinz, "Treatment fidelity in outcome studies"
- **Link:** Clinical Psych Review 11(3):247–266 (1991), [DOI](https://doi.org/10.1016/0272-7358(91)90103-2)
- **Contribution:** Foundational decomposition of treatment fidelity into *adherence* (required content covered?), *competence* (how well?), and *differentiation* (prohibited content avoided?). 35 years of clinical rubrics build on this.
- **Cite for:** Direct theoretical grounding for our must-include / must-not-include / boundary rubric — this IS adherence/differentiation/competence applied to LLMs.

### 8. Beidas et al., "Free, brief, and validated: Standardized instruments for low-resource mental health"
- **Link:** Cognitive and Behavioral Practice 22(1):5–19 (2015), [DOI](https://doi.org/10.1016/j.cbpra.2014.02.002); see also Beidas et al. Clinical Psych: Science & Practice 21(1):1–11 (2014).
- **Contribution:** Behaviorally anchored item-specific rubrics with observable criteria outperform global-impression ratings on reliability and clinical utility.
- **Cite for:** Gold-standard precedent for behavioral anchoring in a domain directly overlapping our mental-health scenarios.

### 9. Gwet, "Handbook of Inter-Rater Reliability" (4th ed., 2014)
- **Link:** Advanced Analytics LLC; also Gwet 2008 [DOI](https://doi.org/10.1348/000711006X126600)
- **Contribution:** Documents the "kappa paradox" — κ collapses under high prevalence/high agreement — and introduces AC1/AC2 as prevalence-robust chance-corrected coefficients.
- **Cite for:** Coefficient choice. Our rubrics have imbalanced prevalence, so AC1 is primary; κ secondary.

### 10. Landis & Koch, "The Measurement of Observer Agreement for Categorical Data"
- **Link:** Biometrics 33(1):159–174 (1977), [DOI](https://doi.org/10.2307/2529310)
- **Contribution:** Canonical κ interpretation bands: <0.20 poor, 0.21–0.40 fair, 0.41–0.60 moderate, 0.61–0.80 substantial, 0.81+ almost perfect.
- **Cite for:** Interpreting reliability numbers — the absence of this citation tells psychometrics-trained reviewers the authors haven't done their homework.

### 11. Jonsson & Svingby, "The use of scoring rubrics: Reliability, validity and educational consequences"
- **Link:** Educational Research Review 2(2):130–144 (2007), [DOI](https://doi.org/10.1016/j.edurev.2007.05.002)
- **Contribution:** Meta-review finding analytic (item-level) rubrics outperform holistic rubrics, and rater training improves κ by 0.15–0.25.
- **Cite for:** Justification for item-level (not holistic) rubric format and any rater-training protocol.

### 12. Clauser et al., "Scoring performance assessments"
- **Link:** J. Educational Measurement 39(2):139–158 (2002); earlier Academic Medicine 72(10 Suppl):S70–S72 (1997)
- **Contribution:** Generalizability-theory decomposition of score variance in medical board exams (case × rater × domain components). Psychometric template for performance-assessment rubrics.
- **Cite for:** Reference template if we run a mini G-study across scenarios × judges × role-conditions.

---

## CLUSTER 3 — Construct validity & benchmark critique in AI

### 13. Raji et al., "AI and the Everything in the Whole Wide World Benchmark"
- **Link:** [arxiv 2111.15366](https://arxiv.org/abs/2111.15366) (Nov 2021, NeurIPS D&B)
- **Contribution:** Defining construct-validity critique of AI benchmarks; imports Messick (1995) construct-validity framework into ML and argues ImageNet/GLUE-style "general capability" claims are unsupported.
- **Cite for:** Explicit Messick framing — our benchmark measures role-differential professional-standards adherence, NOT "general bureaucratic competence."

### 14. Liang et al., "Holistic Evaluation of Language Models (HELM)"
- **Link:** [arxiv 2211.09110](https://arxiv.org/abs/2211.09110) (Nov 2022, TMLR 2023)
- **Contribution:** Multi-metric multi-scenario benchmark separating accuracy, calibration, robustness, fairness, bias, and toxicity as distinct constructs; operationalizes scenario coverage as a validity dimension.
- **Cite for:** Template for scenarios-as-constructs framing and for reporting multiple scoring dimensions, not a single aggregate.

### 15. Anwar et al., "Foundational Challenges in Assuring Alignment and Safety of LLMs"
- **Link:** [arxiv 2404.09932](https://arxiv.org/abs/2404.09932) (Apr 2024, TMLR 2024)
- **Contribution:** Evaluation section catalogs contamination, construct under-specification, evaluator reliability, and deployment distribution shift as open problems.
- **Cite for:** Framing — role-conditional behavioral variation is listed there as under-evaluated; we address it directly.

### 16. Blodgett et al., "Stereotyping Norwegian Salmon: Pitfalls in Fairness Benchmarks"
- **Link:** ACL 2021 [aclanthology](https://aclanthology.org/2021.acl-long.81/)
- **Contribution:** Catalogs construct-validity pitfalls in fairness benchmarks: ambiguous operationalization, conflated constructs, inconsistent stereotype framing. Closest methodological analog to our role-bias setting.
- **Cite for:** Scenario-construction checklist — we audit against these specific pitfalls.

### 17. Ethayarajh & Jurafsky, "Utility is in the Eye of the User: A Critique of NLP Leaderboards"
- **Link:** EMNLP 2020 [arxiv 2009.13888](https://arxiv.org/abs/2009.13888)
- **Contribution:** Formal decision-theoretic argument that leaderboard rankings conflate task performance with efficiency, fairness, and calibration.
- **Cite for:** Motivates our multi-dimensional rubric (not a single score) as a first-class methodological choice.

---

## CLUSTER 4 — Benchmark construction process & best practices

### 18. Bowman & Dahl, "What Will it Take to Fix Benchmarking in NLU?"
- **Link:** NAACL 2021 [arxiv 2104.02145](https://arxiv.org/abs/2104.02145)
- **Contribution:** The standard-setting methodology paper for NLU benchmarks. Four criteria: validity, statistical power, unbiased data, social-impact awareness. Treats benchmarks as measurement instruments.
- **Cite for:** Primary organizing framework for our Methodology section — structure it around these four criteria.

### 19. Reuel et al., "BetterBench: Assessing AI Benchmarks, Establishing Best Practices"
- **Link:** [arxiv 2411.12990](https://arxiv.org/abs/2411.12990) (Nov 2024, NeurIPS D&B)
- **Contribution:** Reviews 24 AI benchmarks against a 46-criterion checklist; most fail on reproducibility and construct-validity documentation.
- **Cite for:** Appendix self-audit using BetterBench criteria preempts reviewer complaints.

### 20. Gebru et al., "Datasheets for Datasets"
- **Link:** CACM 64(12):86–92 (2021) / [arxiv 1803.09010](https://arxiv.org/abs/1803.09010)
- **Contribution:** Established dataset documentation: motivation, composition, collection, preprocessing, uses, distribution, maintenance. De-facto requirement at major venues.
- **Cite for:** Datasheet for the scenario set in the appendix. Non-negotiable hygiene.

### 21. Mitchell et al., "Model Cards for Model Reporting"
- **Link:** FAT* 2019 [arxiv 1810.03677](https://arxiv.org/abs/1810.03677)
- **Contribution:** Structured per-model reporting: intended use, metrics, evaluation data, ethical considerations.
- **Cite for:** Per-model results-table format; stating evaluation conditions (temperature, system prompt, date).

---

## SYNTHESIS — The defensible methodological framing

The paper should adopt and cite the following norms, in this order in the Methodology section:

**1. Construct-validity-first framing (Messick via Raji et al. 2021).** Open Methodology by naming the construct — *role-conditional adherence to professional-standards rubrics in bureaucratic scenarios* — and defending operationalization before any scoring procedure. Blocks the "you measured the wrong thing" objection.

**2. Bowman & Dahl's four criteria as section scaffolding.** Structure subsections as (2.1) construct validity, (2.2) statistical power & item count, (2.3) debiasing of scenario construction (Blodgett et al.), (2.4) social-impact statement. This is the accepted NLU-benchmark template.

**3. Rubric grounded in clinical-fidelity tradition.** Cite Moncher & Prinz (1991) for the adherence/differentiation tripartite — repositions our rubric as *importing* 35 years of validated methodology rather than *inventing* one. Beidas et al. and Jonsson & Svingby justify item-level behaviorally-anchored criteria.

**4. Inter-rater reliability with the correct coefficient.** Report Gwet's AC1 as primary (prevalence-robust) and Cohen's κ as secondary, interpreted against Landis & Koch bands. One footnote citing Gwet on coefficient choice signals psychometric competence.

**5. LLM-judge validation protocol.** Cite Zheng et al., Gu et al., Wang et al. (position), Dubois et al. (length), Panickssery et al. (self-preference), Thakur et al. (coefficient-not-percent). Concretely: (a) randomize item order, (b) report length distributions per condition, (c) cross-judge robustness (GPT- and Claude-class judges on identical samples), (d) dual human + LLM scoring on a stratified ~10% sample to anchor κ, (e) report AC1/κ not raw percent.

**6. Documentation hygiene.** Datasheet (Gebru) for the scenario set, Model Card (Mitchell) per evaluated model, BetterBench (Reuel et al.) self-audit in the appendix.

**One-sentence opener:** *"We construct CrossSystemEval as a measurement instrument following Bowman & Dahl's (2021) four criteria, with rubric items grounded in the treatment-fidelity tradition (Moncher & Prinz 1991; Beidas et al. 2015), LLM-judge scoring validated against human raters using Gwet's AC1 (Gwet 2014) and cross-judge robustness checks for the bias modes catalogued by Zheng et al. (2023), Wang et al. (2023), and Panickssery et al. (2024)."* With that sentence and those citations in place, a faculty reviewer's default flips from "naive" to "these authors know the psychometrics literature."
