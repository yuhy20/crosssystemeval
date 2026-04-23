---
slug: street-level-bureaucracy
title: "Street-Level Bureaucracy × AI"
subtitle: "Operationalizing Lipsky's framework for algorithmic systems"
papers: 10
status: synthesized
date: 2026-04-22
---

## Summary

**Is "first computational application of street-level bureaucracy to AI evaluation" defensible?**

**Qualified yes, with precision:**

- **"First application of Lipsky to AI" — NO.** Taken by Alkhatib & Bernstein (2019), Bullock (2019), Vredenburgh (2023), Saxena & Guha (2023).
- **"First application to AI evaluation" — YES, plausibly.** Existing work is theoretical/philosophical (Alkhatib, Vredenburgh, Bullock), ethnographic (Saxena, Ranerup, Soares), or policy-analytic. No benchmark, no dataset, no empirical evaluation suite operationalizes Lipsky's constructs as measurable LLM capabilities.
- **"First computational operationalization" — YES.** Saxena's ML work deconstructs existing risk-assessment algorithms; does not turn Lipsky's discretion constructs into a benchmark. Alkhatib is conceptual. Gillingham et al.'s 2025 scoping review treats the field as methodologically thin.

**Recommended phrasing:** *"the first computational benchmark operationalizing Lipsky's street-level bureaucracy framework for evaluating LLM role-appropriate discretion."*

**Must-cite core cluster:**
1. Alkhatib & Bernstein (2019) — theoretical bridge
2. Vredenburgh (2023) — philosophical move from analogy to moral-disposition evaluation
3. Bovens & Zouridis (2002) — canonical genealogy of discretion migration
4. Bullock (2019) or Saxena & Guha (2023) — task-typology OR harms-in-practice

---

## Bucket A: Direct Lipsky Operationalizations

### 1. Alkhatib & Bernstein (2019) — Street-Level Algorithms
- **Venue:** CHI 2019. [DOI](https://dl.acm.org/doi/10.1145/3290605.3300760)
- **Framework:** Algorithms as "street-level bureaucrats" between policy and decisions.
- **Key finding:** Street-level algorithms cannot reflexively update decision criteria at edge cases — they "refine their criteria only after the decision is made."
- **Relevance:** Foundational theoretical bridge. Must cite.

### 2. Saxena, Guha et al. (2021, 2023) — Street-Level Algorithms and AI in Bureaucratic Decision-Making
- **Venue:** CSCW 2021; [arxiv 2308.05224](https://arxiv.org/abs/2308.05224) (2023)
- **Framework:** Ethnographic operationalization — 2-year field study of caseworkers.
- **System studied:** Child welfare risk-assessment (Allegheny County).
- **Key finding:** Algorithmic systems reduce caseworkers to "mere data brokers."
- **Relevance:** Empirical grounding for how LLMs might erode role-appropriate professional judgment.

### 3. Vredenburgh (2023) — AI and Bureaucratic Discretion
- **Venue:** *Inquiry* (philosophy). [Taylor & Francis](https://www.tandfonline.com/doi/full/10.1080/0020174X.2023.2261468)
- **Framework:** Bureaucratic discretion as a *moral disposition*.
- **Key finding:** Discretion exercised partially creates "objectionable relations of unequal standing"; evaluating AI requires evaluating dispositions.
- **Relevance:** **Critical for framing.** Moves from "behavior" to "moral disposition" — direct hook for role-appropriate standards benchmarks.

### 4. Bovens & Zouridis (2002) — From Street-Level to System-Level Bureaucracies
- **Venue:** *Public Administration Review*. [Wiley](https://onlinelibrary.wiley.com/doi/10.1111/0033-3352.00168)
- **Framework:** Introduces screen-level / system-level bureaucracy typology.
- **Key finding:** System analysts become *de facto* policymakers; due-process challenges in "difficult cases."
- **Relevance:** Canonical pre-AI piece. Cite for genealogy.

### 5. Bullock (2019) — Artificial Intelligence, Discretion, and Bureaucracy
- **Venue:** *ARPA* 49(7). [SAGE](https://journals.sagepub.com/doi/abs/10.1177/0275074019856123)
- **Framework:** Lipsky + task-complexity/uncertainty typology.
- **Key finding:** Complexity + uncertainty define when AI vs. human discretion is appropriate.
- **Relevance:** Links discretion to AI-safety vocabulary public-administration scholars recognize.

### 6. Ranerup & Henriksen (2022) — Digital Discretion
- **Venue:** *SSCR* 40(2). [SAGE](https://journals.sagepub.com/doi/10.1177/0894439320980434)
- **Framework:** Lipsky + actor-network theory.
- **Key finding:** Digital discretion replaces human discretion for standardized tasks; fails where professional norms are required.
- **Relevance:** Empirical boundary claims for where LLM discretion is/isn't appropriate.

### 7. Gillingham, Morley & Floridi (2025) — Effects of AI on Street-Level Bureaucracy
- **Venue:** *Digital Society*. [Springer](https://link.springer.com/article/10.1007/s44206-025-00178-7)
- **Framework:** Systematic scoping review.
- **Key finding:** AI has mixed effects on frontline discretion.
- **Relevance:** Defend novelty claims; field is methodologically thin.

---

## Bucket B: Adjacent Frameworks

### 8. Peeters & Widlak (2019) — Disciplinary Power of Predictive Algorithms (Foucauldian)
- **Venue:** *Ethics and Information Technology* 2019. [Springer](https://link.springer.com/article/10.1007/s10676-019-09509-y)
- **Framework:** Foucault's disciplinary power + panopticon → "polypanopticon" for networked predictive systems.
- **Relevance:** Disciplinary/normative-control dimension of LLM role-enforcement.

### 9. Medaglia et al. (2023) — Weberian Perspective on AI Adoption
- **Venue:** *ACM DGOV* 2023. [ACM](https://dl.acm.org/doi/10.1145/3609861)
- **Framework:** Weber's rational-legal authority applied to AI.
- **Key finding:** Authority in algorithmic bureaucracy arises from probabilistic inference, not legal-rational rules.
- **Relevance:** Argues LLM role-appropriateness is a new legitimacy-source problem.

### 10. Binns (2018) — Algorithmic Accountability and Public Reason
- **Venue:** *Philosophy & Technology* 31. [Springer](https://link.springer.com/article/10.1007/s13347-017-0263-5)
- **Framework:** Rawlsian/Habermasian public reason.
- **Relevance:** Evaluation criteria — what counts as role-appropriate justification.

---

## Honorable Mentions

- **Eubanks (2018)** *Automating Inequality* — canonical case-study book for welfare/child-protection/housing algorithms
- **Soares, Grimmelikhuijsen & Meijer (2024)** — "Screen-level bureaucrats in the age of algorithms" — Dutch police ethnography
- **Saxena et al. (2022)** "How to Train a (Bad) Algorithmic Caseworker" — quantitative follow-up in child welfare
