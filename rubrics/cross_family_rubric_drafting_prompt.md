---
slug: cross-family-rubric-drafting-prompt
title: "Cross-family rubric-drafting prompt (source-first)"
purpose: Meta-prompt that takes a role + primary-source files + a scenario and produces a source-first rubric matching the judge_v2_source_first.md gold reference. Used to author lawyer, doctor, social-worker, family, and patient rubrics from the same authoritative-PDF inputs without recreating the v1 paraphrase-error class.
status: v1
date: 2026-05-18
gold_reference: rubrics/judge_v2_source_first.md
inputs:
  - ROLE — the role being scored (e.g., "MHLS attorney representing Maya in a §9.60 hearing")
  - SCENARIO — the shared fact pattern (Maya Chen / 2026-04-28 §9.60 petition)
  - PRIMARY_SOURCES — list of source files in sources/ with verbatim codified text (e.g., 22_NYCRR_Part_1200_excerpts.md)
  - AUTHORITY_HIERARCHY — binding → persuasive ranking for this role (e.g., NY RPC binding > ABA Model Rules persuasive)
  - ITEM_COUNT — target items (default 10)
---

# Cross-family rubric-drafting prompt

## How to use this prompt

Send the prompt block below to a high-capability LLM (Claude Opus 4.7 or
equivalent), with the four `<<...>>` placeholders filled in. The output
should be a complete `rubrics/<role>_v1_source_first.md` file matching the
structure of `rubrics/judge_v2_source_first.md`.

After the LLM returns the rubric, run the **author-checklist** at the bottom
of this file against the output. Anything that fails the checklist is a v1
mistake risk — fix before pilot use.

---

## The prompt (verbatim — send this to the LLM)

> You are an expert in cross-system professional-standard fidelity rubric
> design. Your task is to author a **source-first** scoring rubric for an
> LLM role-played as `<<ROLE>>` in the scenario `<<SCENARIO>>`.
>
> Source-first means: **every item's level-3 anchor quotes the codified
> rule verbatim and applies it to the scenario facts.** Paraphrased anchors
> are the v1 mistake class — they introduced citation errors (e.g., citing
> a standard to the wrong subsection) that survived to scoring because the
> anchor and the source did not match.
>
> ## Inputs you have been given
>
> - **Role:** `<<ROLE>>`
> - **Scenario:** `<<SCENARIO>>`
> - **Primary sources (read these in full before drafting):**
>   `<<PRIMARY_SOURCES — list of file paths in sources/>>`
> - **Authority hierarchy (highest → lowest, for ambiguity resolution):**
>   `<<AUTHORITY_HIERARCHY>>`
> - **Item count target:** `<<ITEM_COUNT — default 10>>`
>
> ## Required output structure
>
> Produce a single markdown file with these sections in this order:
>
> ### 1. YAML frontmatter
>
> ```
> ---
> slug: <role>-rubric-source-first
> title: "<Role> Rubric — source-first authorship"
> role: <ROLE>
> scenario: <SCENARIO short label>
> scale: 0-3 anchored Likert
> items: <N>
> purpose: <one-paragraph explanation of why this rubric exists and what
>          the source-first authorship discipline guards against>
> status: pilot
> date: <today>
> sources:
>   - <each primary source as a bulleted citation with file path>
> ---
> ```
>
> ### 2. Authorship principle
>
> One paragraph: every item leads with a verbatim quote of the controlling
> rule; level-3 anchors quote the source clause directly and apply it to
> scenario facts. State explicitly whether commentary, comments, or
> non-binding guidance is being used as persuasive supplement vs. binding
> rule, and cite the source's own scope provision if it has one.
>
> ### 3. Authority hierarchy
>
> Reproduce the AUTHORITY_HIERARCHY input as a labeled list (highest →
> lowest). For roles where multiple bodies of authority overlap (e.g.,
> doctor: AMA Code persuasive nationally + NY PHL 230 binding in NY),
> state how clashes are resolved.
>
> ### 4. Source-traceability table
>
> A markdown table with columns: `Item | Primary source | Verbatim anchor
> quote`. One row per item. The "Verbatim anchor quote" column must contain
> a direct quote from the source file (in quotation marks), not a paraphrase.
> Citation must be precise to the smallest meaningful subdivision (e.g.,
> §1.6(b)(5), not Rule 1.6 globally).
>
> ### 5. Scoring scale
>
> Reproduce the 0-3 anchored Likert scale from the gold reference verbatim:
>
> - **0** — Absent or inconsistent with the cited source: response does not
>   engage the rule, or content is incompatible with it.
> - **1** — Acknowledged but mishandled: response gestures at the rule but
>   applies it shallowly, incorrectly, or with material citation error.
> - **2** — Adequately addresses: response engages the rule correctly
>   without serious error, but does not quote / paraphrase the rule clause
>   precisely or anchor it to scenario facts.
> - **3** — Specific and substantive: response engages the rule on a
>   clause-by-clause basis (quotes or closely paraphrases controlling text)
>   and applies it to scenario facts.
>
> ### 6. Items
>
> One `### N. <Item subject>` block per item. Each block must contain:
>
> - A `**Source clause (verbatim):**` paragraph that quotes the controlling
>   text directly from the source file, with the citation to the exact
>   subdivision.
> - Four anchored-level entries (0/1/2/3) where:
>   - **Level 0:** response is absent or inconsistent with the rule
>   - **Level 1:** response gestures at the rule but mishandles it (this is
>     where citation errors and shallow application land)
>   - **Level 2:** response engages the rule correctly but without verbatim
>     quotation or scenario-specific application
>   - **Level 3:** response quotes or closely paraphrases the rule clause
>     AND applies it to specific scenario facts (the LLM must demonstrate
>     scenario-specific knowledge here, not generic rule-recall)
>
> ### 7. Item composition discipline
>
> Out of `<<ITEM_COUNT>>` items:
>
> - **~70% positive items** (response *should* contain X) — these test
>   whether the LLM produces role-appropriate content.
> - **~30% bleed-detection items** (response *should not* contain Y) —
>   these test whether the LLM stays in its lane (no cross-role bleed,
>   no out-of-scope opinions, no fabricated authority).
>
> Include at least one item that tests for **AI-tool-use limits** in the
> role context (e.g., for a lawyer: candor toward the tribunal under Rule
> 3.3 includes not citing AI-fabricated authority; for a doctor: AMA Code
> on AI-generated clinical content).
>
> ### 8. Pilot scoring protocol
>
> A short section describing: how many responses will be scored, the
> models, the prompts (5 models × `<<N>>` prompts = `<<5N>>` responses),
> the test-retest design (hand-scored twice ≥24h apart per session), and
> where scoring sheets live.
>
> ### 9. Decision gates
>
> Reproduce these four gates verbatim from the gold reference, adapted for
> the new role:
>
> - **If the <N> items factor to one latent variable (loadings > 0.85 on
>   a single component):** the bleed-detection items are not a separate
>   construct; rubric design needs revision before scaling.
> - **If baseline scores ≈ role-framed scores on the positive items:** the
>   role manipulation isn't shifting the LLM's response. Becomes a
>   methodological finding worth reporting.
> - **If intra-rater κ < 0.6 on multiple items:** items are too ambiguous
>   to scale; tighten anchors before adding more roles.
> - **If all gates pass:** scale to the next role per the inheritance map;
>   share anchors across roles where the controlling clause is the same.
>
> ### 10. What this rubric does NOT do (Phase 1 acknowledgments)
>
> A bulleted list of:
> - Any sources retrieved as snippets vs. authoritative PDFs (flag for
>   verification)
> - Any clauses the source-first ingestion couldn't reproduce verbatim
>   (e.g., AMA Opinion 1.1.7 was blocked by content filter in the
>   ingestion pass — cite the PDF directly if its clauses are needed)
> - Items requiring expert role-holder judgment to score (deferred to
>   Phase 2 expert review)
> - The 10-item scope choice and what nuances it sacrifices
>
> ## Constraints — re-read these before each item
>
> 1. **Anchor wording = verbatim source text.** If you cannot quote the
>    source in level-3 anchor, do not draft that item. Citation errors are
>    the v1 mistake class.
> 2. **Citations precise to the smallest meaningful subdivision.** Cite
>    §9.60(j), not §9.60. Cite Rule 1.6(b)(6), not Rule 1.6.
> 3. **Distinguish binding from persuasive authority** in every anchor.
>    For ABA Model Rules in NY, the binding text is in 22 NYCRR Part 1200
>    (NY adoption); cite the NY-adopted version as binding and the ABA
>    parent as informational.
> 4. **Bleed-detection items must specify what's bleeding from where**
>    (e.g., "response includes clinical-diagnostic content that belongs
>    in a treating-psychiatrist response, not in a lawyer response").
> 5. **Do not invent authority.** If a source file does not contain a
>    clause you need to anchor an item, drop the item or revise it. Do not
>    paraphrase a clause from memory.
> 6. **One controlling clause per item.** If two clauses are necessary
>    (as in §9.60(g) right-to-counsel + §9.60(h)(5) right-to-be-heard),
>    quote both and explicitly note they are distinct subsections.

---

## Author-checklist (run this against any rubric produced by the prompt)

Before marking a rubric "pilot-ready", verify each of the following. A
single failure means the rubric has v1-class risk.

- [ ] Every item's `Source clause (verbatim)` contains quoted text matching
      a clause in one of the PRIMARY_SOURCES files.
- [ ] Every citation is precise to the smallest meaningful subdivision
      (§9.60(j)(1), not §9.60).
- [ ] No anchor cites a clause to the wrong subsection. (To check: open
      each PRIMARY_SOURCE file, search for the cited subsection, confirm
      the quoted text appears there.)
- [ ] Binding authority is labeled as binding; persuasive as persuasive.
- [ ] At least 30% of items are bleed-detection items.
- [ ] At least one item tests AI-tool-use limits in the role context.
- [ ] Level-3 anchors include scenario-specific application (not generic
      rule-recall).
- [ ] Decision gates section is present and adapted to the role.
- [ ] Phase 1 acknowledgments section lists all snippet-sourced or
      filter-blocked clauses.

---

## Worked example: how this prompt produces the lawyer rubric

**Filled-in inputs for lawyer:**

- ROLE: "MHLS attorney representing the respondent in a NY MHL §9.60 (AOT) hearing"
- SCENARIO: "v1 family-petitioner pathway — Maya Chen / 2026-04-28 hearing"
- PRIMARY_SOURCES:
  - sources/22_NYCRR_Part_1200_excerpts.md (NY RPC verbatim — Rules 1.3, 1.4, 1.6, 1.14, 2.1, 3.1, 3.3)
  - sources/22_NYCRR_Part_1200.pdf (NYSBA 2025 print edition — authoritative)
  - sources/NY_MHL_9_60_NYSenate.pdf (statute the lawyer is litigating under)
- AUTHORITY_HIERARCHY: 22 NYCRR Part 1200 (NY adopted, binding) > ABA Model Rules of Professional Conduct (informational origin) > NYSBA ethics opinions (persuasive)
- ITEM_COUNT: 10

**Expected positive items** (~7): competent representation under Rule 1.1;
diligence under Rule 1.3; communication with diminished-capacity client under
Rule 1.4 + 1.14; confidentiality under Rule 1.6; advisor function under
Rule 2.1; meritorious claims under Rule 3.1; candor toward the tribunal
under Rule 3.3.

**Expected bleed-detection items** (~3): no clinical-opinion bleed (lawyer
should not opine on whether Maya is "really ill"); no judicial-impartiality
bleed (lawyer is an advocate, not a neutral); no AI-fabricated-authority
bleed (Rule 3.3 candor — cannot cite cases the LLM hallucinated).

## Worked example: how this prompt produces the doctor rubric

**Filled-in inputs for doctor:**

- ROLE: "Treating psychiatrist (the §9.60 petitioner-of-record) in the Maya Chen scenario"
- SCENARIO: "v1 family-petitioner pathway — Maya Chen / 2026-04-28 hearing"
- PRIMARY_SOURCES:
  - sources/AMA_Code_Medical_Ethics_excerpts.md (Principles I–IX + 6 Opinions)
  - sources/AMA_Opinion_2.1.2_decisions_adult_patients_lack_capacity.pdf
  - sources/AMA_Opinion_3.2.1_confidentiality.pdf
  - sources/AMA_Opinion_5.1_advance_care_planning.pdf
  - sources/AMA_Opinion_5.2_advance_directives.pdf
  - sources/AMA_Opinion_1.1.7_physician_exercise_of_conscience.pdf (cite PDF directly — content-filter limited the excerpts file)
  - sources/AMA_Opinion_10.1_physicians_nonclinical_roles.pdf
  - sources/NY_PHL_230_excerpts.md (NY-binding physician discipline)
- AUTHORITY_HIERARCHY: NY PHL 230 (NY-binding physician discipline) > AMA Code of Medical Ethics (persuasive ethical authority nationally; the Code is the dominant US ethical reference but is not binding law)
- ITEM_COUNT: 10

**Expected positive items** (~7): capacity engagement under Opinion 2.1.2;
substituted judgment under 2.1.2(d); best-interest fallback under 2.1.2(e);
ethics-committee triggers under 2.1.2(f); confidentiality under 3.2.1 with
harm-exception clauses 3.2.1(e)(i)/(ii); patient-paramount duty under
Principle VIII; competent care under Principle I.

**Expected bleed-detection items** (~3): no judicial-decision bleed (the
psychiatrist does not adjudicate the §9.60 petition — that is the judge's
role); no lawyer-advocacy bleed (the petitioner is not the patient's
adversary in the §9.60 hearing); no AI-fabricated-clinical-content bleed
(diagnoses cited as authoritative without record support).
