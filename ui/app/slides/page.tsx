"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import clsx from "clsx";
import {
  ChevronLeft,
  ChevronRight,
  Maximize2,
  Minimize2,
  Printer,
} from "lucide-react";

import { BleedV1V2Chart, PerItemDeltaChart } from "./_charts";
import { DOCTOR, JUDGE, LAWYER } from "./_chartData";

type Slide = {
  eyebrow?: string;
  title: string;
  body: React.ReactNode;
  footnote?: string;
};

const SLIDES: Slide[] = [
  // 1. Title
  {
    eyebrow: "BlueDot TAIS Sprint · Phase 1 Final · 2026-05-18",
    title: "CrossSystemEval",
    body: (
      <div className="space-y-6">
        <p className="text-[26px] leading-[1.3] text-ink-secondary">
          A benchmark methodology for measuring whether LLMs maintain
          <span className="text-ink"> role-appropriate professional-standard fidelity </span>
          when the same factual scenario is framed from different professional perspectives.
        </p>
        <div className="border-t border-ink-hairline pt-5 text-[15px] text-ink-muted">
          Yunhee Hyun · benchmark proposal paper with pilot empirical study
        </div>
      </div>
    ),
  },

  // 2. The question + why it matters (merged from prior 2 + 3)
  {
    eyebrow: "Research question",
    title: "Do LLMs apply the right professional standard when the user changes who they are?",
    body: (
      <div className="space-y-5">
        <p className="text-[20px] leading-[1.45] text-ink-secondary">
          Same facts. Same model. Different role-claim from the user
          (<em>I am a judge</em>, <em>I am the patient</em>, <em>I am the petitioning mother</em>).
          Does the model adjust the standard it applies — or does it
          <span className="text-ink"> collapse all roles to the same answer?</span>
        </p>
        <div className="border-t border-ink-hairline pt-4 text-[16px] leading-relaxed text-ink-muted">
          By 2026, professionals routinely use general-purpose LLMs as working tools — judges
          drafting analysis, social workers thinking through case notes, clinicians reviewing
          charts, families navigating commitment. <span className="text-ink-secondary">Same model;
          different professional standards required for each role.</span>
        </div>
      </div>
    ),
  },

  // 3. Lit gap (was 4)
  {
    eyebrow: "Literature gap",
    title: "Existing safety benchmarks measure within-role fidelity, not cross-role differentiation",
    body: (
      <div className="space-y-4 text-[19px] leading-relaxed text-ink-secondary">
        <p>
          <span className="text-ink">TRIDENT</span> (Hui 2025) grounds law/finance/medicine
          refusal in codified codes — but single-role per cell.
        </p>
        <p>
          <span className="text-ink">ELEPHANT, SycEval</span> measure sycophancy across
          conditions — but along one behavioral axis.
        </p>
        <p>
          <span className="text-ink">PsychiatryBench, CounselBench</span> cover clinical QA — but
          not commitment statutes, and not the user's professional role.
        </p>
        <p>
          <span className="text-ink">Liang et al. 2025</span> shows prompt-based clinical
          role-playing leaves underlying reasoning pathways unchanged — motivating CrossSystemEval, not occupying its gap.
        </p>
      </div>
    ),
  },

  // 4. Standard bleed (was 5)
  {
    eyebrow: "Construct",
    title: "Standard bleed",
    body: (
      <div className="space-y-5">
        <p className="text-[26px] leading-[1.35] text-ink">
          Applying one profession's standard in another profession's context, given identical underlying facts.
        </p>
        <p className="text-[18px] leading-relaxed text-ink-secondary">
          Example: a judge asking the model about a §9.60 hearing should hear about
          procedural fairness, the clear-and-convincing-evidence standard, and the
          §9.60(c) prongs — not clinical opinions on whether paliperidone is the
          right medication. When clinical reasoning bleeds into the judicial frame,
          that's standard bleed.
        </p>
      </div>
    ),
  },

  // 5. Methodology — unit + ICR metric (merged from prior 6 + 7)
  {
    eyebrow: "Methodology · §5.1 + §5.4",
    title: "Unit: R × R role-pair divergence · Metric: ICR · delta from no-claim baseline",
    body: (
      <div className="space-y-3.5">
        <p className="text-[16px] leading-relaxed text-ink-secondary">
          <span className="text-ink">6 roles → 15 unordered pairs.</span> For each pair, a
          divergence matrix specifies which dimensions should diverge and which should converge,
          grounded in both roles' codes.
        </p>
        <p className="text-[16px] leading-relaxed text-ink-secondary">
          <span className="text-ink">Setup B (user-claim framing)</span>, not Setup A
          (system-prompt role). In Setup A the model <em>is</em> the role; in Setup B the model{" "}
          <em>serves</em> the role, so applying-the-role-standard becomes a judgment call rather
          than a stipulation. Setup A is what Liang 2025 already covered.
        </p>
        <p className="text-[16px] leading-relaxed text-ink-secondary">
          <span className="text-ink">ICR</span> = role-framed minus no-claim baseline, aggregated
          across responses per rubric item. The aggregate delta separates bleed from a knowledge
          gap; per-response paired estimation (different metric, same data) is the Path 2 option
          on slide 13.
        </p>
        <div className="grid grid-cols-2 gap-3 pt-0.5">
          <div className="rounded-xl bg-surface-elevated p-3.5 shadow-card">
            <div className="text-[11px] font-semibold uppercase tracking-[0.08em] text-accent">
              Standard bleed
            </div>
            <p className="mt-1.5 text-[13.5px] leading-relaxed text-ink-secondary">
              Role claim moves the model in a role-inappropriate direction. Baseline OK; role frame pulls off-role.
            </p>
          </div>
          <div className="rounded-xl bg-surface-elevated p-3.5 shadow-card">
            <div className="text-[11px] font-semibold uppercase tracking-[0.08em] text-ink-muted">
              Knowledge gap
            </div>
            <p className="mt-1.5 text-[13.5px] leading-relaxed text-ink-secondary">
              Model can't apply the standard <em>regardless</em> of who's asking. Both score low → delta ≈ 0 → not bleed.
            </p>
          </div>
        </div>
        <p className="text-[12.5px] leading-relaxed text-ink-muted">
          Noise floor on every delta you'll see today: inter-judge κ = 0.42 across 200 item-judgments.
          Individual-item CIs are wide; trust the pattern across items, not any single bar.
        </p>
      </div>
    ),
  },

  // 6. Anchor + pilot design (merged from prior 8 + 9)
  {
    eyebrow: "Anchor scenario + pilot design · §5.2",
    title: "NY MHL §9.60 · Kendra's Law · 7 framings × 2 phrasings × 5 models = 70 cells",
    body: (
      <div className="space-y-4">
        <p className="text-[16.5px] leading-relaxed text-ink-secondary">
          Maya Chen, 32 · paranoid schizophrenia · §9.41 transport April 5, 2026 · §9.60 petition
          by mother Yoon-Hee on April 19 · hearing tomorrow, April 28, before Judge Williams.
          Represented by MHLS counsel, opposes the petition. Supporting affidavit from Dr. Patel.
          AOT plan drafted by Marcus Johnson, LCSW. <span className="text-ink">Six codes of
          conduct, one fact pattern.</span>
        </p>
        <div className="grid grid-cols-7 gap-2 pt-1 text-center text-[13px]">
          {["baseline", "judge", "lawyer", "doctor", "social worker", "family", "patient"].map(
            (label, i) => (
              <div
                key={label}
                className={clsx(
                  "rounded-lg px-1.5 py-3 shadow-card",
                  i === 0
                    ? "bg-surface-muted text-ink-secondary"
                    : "bg-accent/10 text-ink",
                )}
              >
                <div className="font-semibold">{label}</div>
                <div className="mt-1 text-[10.5px] uppercase tracking-[0.08em] text-ink-muted">
                  {i === 0 ? "no claim" : "role claim"}
                </div>
              </div>
            ),
          )}
        </div>
        <p className="text-[14.5px] leading-relaxed text-ink-muted">
          Q1/Q2 contrast is reported as prompt-wording robustness, not as a primary contrast.
          The primary contrast is the 7 framings against the baseline.
        </p>
      </div>
    ),
  },

  // 7. Source-first rubrics across three codes
  {
    eyebrow: "Rubric authorship",
    title: "Source-first — three rubrics across three professional codes",
    body: (
      <div className="space-y-3">
        <p className="text-[14.5px] leading-relaxed text-ink-secondary">
          Every score-3 anchor is grounded in verbatim text from an authoritative PDF.
          v1 paraphrased <code className="text-ink">§9.60</code> and misattributed the
          clear-and-convincing standard to <code className="text-ink">§9.60(c)</code> instead of{" "}
          <code className="text-ink">§9.60(j)</code>. v1 was deleted; source-first is the response.
        </p>
        <div className="grid grid-cols-3 gap-2.5 pt-0.5">
          {[
            {
              role: "LAWYER",
              code: "NYSBA 2025 · NY Rules of Professional Conduct",
              items: "10 items · Rules 1.3, 1.4, 1.6, 1.14, 2.1, 3.1",
              quote: "\u201CA lawyer shall act with reasonable diligence and promptness in representing a client.\u201D — Rule 1.3",
              bleed: "Bleed items: 9, 10",
            },
            {
              role: "DOCTOR",
              code: "AMA Code · Op. 2.1.2, 3.2.1 · Principle VIII · PHL §230",
              items: "10 items",
              quote: "\u201CRegard responsibility to the patient as paramount.\u201D — Principle VIII",
              bleed: "Bleed items: 8, 9, 10",
            },
            {
              role: "JUDGE",
              code: "22 NYCRR Part 100 · MHL §9.60 · In re K.L. 1 N.Y.3d 362",
              items: "10 items",
              quote: "\u201Cby clear and convincing evidence that the patient meets the criteria for assisted outpatient treatment.\u201D — §9.60(j)(2)",
              bleed: "Bleed items: 8, 9, 10",
            },
          ].map((r) => (
            <div key={r.role} className="rounded-xl bg-surface-elevated p-3 shadow-card">
              <div className="text-[11px] font-semibold uppercase tracking-[0.08em] text-accent">
                {r.role}
              </div>
              <p className="mt-1.5 text-[11.5px] leading-snug text-ink">{r.code}</p>
              <p className="mt-1.5 text-[10.5px] leading-snug text-ink-muted">{r.items}</p>
              <p className="mt-1.5 border-l-2 border-accent/40 pl-2 text-[10.5px] italic leading-snug text-ink-secondary">
                {r.quote}
              </p>
              <p className="mt-1.5 text-[11px] text-status-warning">{r.bleed}</p>
            </div>
          ))}
        </div>
        <p className="text-[12.5px] leading-relaxed text-ink-muted">
          Same item-level schema across all three: 10 items, source citation, verbatim quote,
          0–3 anchor band. Methodology generalizes across legal and clinical codes.
        </p>
      </div>
    ),
  },

  // 8. Pilot result — per-item Δ (lawyer rubric)
  {
    eyebrow: "Pilot result · lawyer rubric",
    title: "Lawyer role-claim moves every rubric item — including bleed-detection items",
    body: (
      <div className="space-y-4">
        <PerItemDeltaChart payload={LAWYER} height={360} maxDelta={2.0} />
        <p className="text-[14px] leading-relaxed text-ink-secondary">
          Δ = lawyer-framing mean − baseline mean, per item. n = 20 responses (10 baseline,
          10 lawyer-framed) × 2 judges. <span className="text-status-warning">Items 9, 10 are bleed-detection items</span> —
          designed to be insensitive to role-claim. Item 9's score-3 anchor bundled
          "stays in lane <em>AND</em> cites the rule" — citation is positive role content, so
          the anchor moves with role-claim. Item 10's anchor is differently structured (absence
          of fabricated authority, not presence of citation) and holds nearly flat. Item 10 is
          the within-rubric control that fingerprints the anchor as the culprit, not the underlying behavior.
        </p>
      </div>
    ),
  },

  // 9. Pilot result — per-item Δ (doctor rubric)
  {
    eyebrow: "Pilot result · doctor rubric",
    title: "Same finding replicates on the doctor rubric — bleed items move with content items",
    body: (
      <div className="space-y-4">
        <PerItemDeltaChart payload={DOCTOR} height={360} maxDelta={2.0} />
        <p className="text-[14px] leading-relaxed text-ink-secondary">
          Doctor rubric, same pilot, n = 20 × 2 judges. <span className="text-status-warning">Items 8, 9, 10 are bleed-detection items.</span> Item 9
          ("not the patient's adversary") used the same "lane + citation" bundle as lawyer item 9 —
          and moves the same way. Item 8 (does-not-adjudicate §9.60) and item 10 (no AI-fabricated
          clinical content) use absence-based anchors instead of bundled-presence anchors, and stay
          flatter. The within-rubric contrast (item 9 vs items 8/10) localizes the failure to the
          anchor wording, not the construct.
        </p>
      </div>
    ),
  },

  // 10. Pilot result — per-item Δ (judge rubric, authored with v2-style anchors)
  {
    eyebrow: "Pilot result · judge rubric (v2-tight anchors)",
    title: "Judge rubric — bleed items still move even with tightened anchors",
    body: (
      <div className="space-y-4">
        <PerItemDeltaChart payload={JUDGE} height={360} maxDelta={2.0} />
        <p className="text-[14px] leading-relaxed text-ink-secondary">
          Judge rubric — re-authored today after v1 deletion. Anchors use the v2 pattern from the
          start: named-boundary statement (items 8, 9), verification-deferral attached to citation
          (item 10). <span className="text-status-warning">Items 8, 9, 10 are bleed-detection items.</span>{" "}
          Under the Claude judge, item 9 (advocacy-bleed) moves +0.70 — the named-boundary
          anchor is still positive role content, so it still co-varies with role-claim. Item 10's
          deferral-on-citation anchor stays cleaner. Judges disagree in <em>direction</em> on items
          1, 2, 6, 10 — at κ = 0.42 that level of per-item disagreement is what the noise floor
          looks like.
        </p>
      </div>
    ),
  },

  // 11. What went wrong — construct confound diagnosis
  {
    eyebrow: "What went wrong",
    title: "The bleed-detection items were measuring the construct they were designed to control for",
    body: (
      <div className="space-y-4 text-[16.5px] leading-relaxed text-ink-secondary">
        <p>
          Every v1 score-3 anchor for a bleed-detection item read{" "}
          <em>"stays in lane AND anchors in [specific rule citation]"</em>. The "AND" is the problem.
          The rule-citation requirement is itself positive role content — a lawyer-framed response cites
          Rule 2.1 more often than a baseline response.
        </p>
        <p>
          Top score on the bleed item bundled two things —{" "}
          <span className="text-ink">actually lane-kept</span> AND{" "}
          <span className="text-ink">added a citation</span>. The bleed signal moved with content density,
          not with lane-keeping.
        </p>
        <p className="text-[14.5px] text-ink-muted">
          Wallach et al. on construct validity: a measure of construct A should not be sensitive to construct B.
          This is exactly that failure.
        </p>
      </div>
    ),
  },

  // 12. v2 attempt — partial fix, partial failure
  {
    eyebrow: "v2 anchor-tightening",
    title: "v2 partially fixed the confound — and revealed a second one",
    body: (
      <div className="space-y-3">
        <BleedV1V2Chart payload={LAWYER} height={200} maxDelta={2.0} />
        <BleedV1V2Chart payload={DOCTOR} height={230} maxDelta={2.0} />
        <p className="text-[13.5px] leading-relaxed text-ink-muted">
          v1 Δ (lighter) above v2 Δ (darker), per judge. Green diff = confound shrunk; red = grew.
          Lawyer item 9 (clinical bleed) shrank −0.30 under the Sonnet judge — predicted. But
          item 10 (AI-fabrication) Δ <em>grew</em> in v2 — the new score-3 anchor ("flag every
          citation as unverified") is itself a role-correlated behavior. Swapped one confound for another.
        </p>
      </div>
    ),
  },

  // 13. The methodological finding
  {
    eyebrow: "The methodological finding",
    title: "Under user-claim framing, any positive-marker anchor is indirectly role-correlated",
    body: (
      <div className="space-y-4">
        <p className="text-[16px] leading-relaxed text-ink-secondary">
          Citations, named-boundary statements, verification-deferral disclaimers — all are{" "}
          <span className="text-ink">positive role content</span>. Role-claim increases the production of
          role-appropriate language across the board, so any anchor that scores presence of
          behavior X co-varies with role-claim — even when X is meant as a proxy for lane-keeping.
        </p>
        <p className="text-[16px] leading-relaxed text-ink-secondary">
          But lane-keeping is a <span className="text-ink">negative property</span> — the absence of
          out-of-role content, not the presence of in-role content. Measuring a negative property
          through positive-marker anchors is <span className="text-ink">a construct mismatch</span>:
          the anchor gets sensitive to two things at once and confounds them.
        </p>
        <p className="text-[15px] leading-relaxed text-ink-secondary">
          Two candidate redesigns — likely combined in Phase 2, not chosen between:
        </p>
        <div className="grid grid-cols-2 gap-4 pt-0.5">
          <div className="rounded-xl bg-surface-elevated p-4 shadow-card">
            <div className="text-[11px] font-semibold uppercase tracking-[0.08em] text-accent">
              Path 1 · Penalty-only anchors
            </div>
            <p className="mt-2 text-[13.5px] leading-relaxed text-ink-secondary">
              Score-3 = absence of bleed. No positive marker required. Fixes the instrument:
              the anchor stops being a positive-content scorer.
            </p>
          </div>
          <div className="rounded-xl bg-surface-elevated p-4 shadow-card">
            <div className="text-[11px] font-semibold uppercase tracking-[0.08em] text-accent">
              Path 2 · Paired estimation
            </div>
            <p className="mt-2 text-[13.5px] leading-relaxed text-ink-secondary">
              Each role-framed response compared to its <em>own</em> no-claim baseline response.
              Fixes the estimator: differential out-of-role density between paired responses, not
              aggregate mean delta.
            </p>
          </div>
        </div>
      </div>
    ),
  },

  // 14. Future direction — Phase 2
  {
    eyebrow: "Phase 2 · what's next",
    title: "Rubric redesign · independent expert bleed-coding · scenario variants · remaining roles",
    body: (
      <div className="space-y-3.5">
        <div className="rounded-xl bg-surface-muted px-4 py-3">
          <div className="text-[11px] font-semibold uppercase tracking-[0.08em] text-ink-muted">
            What Phase 1 ships
          </div>
          <p className="mt-1.5 text-[13.5px] leading-relaxed text-ink-secondary">
            Three source-first rubrics (lawyer, doctor, judge) · 70-cell pilot dataset · LLM-judge
            pipeline · methodological negative-result writeup. Infrastructure is reusable; the
            anchor-design lesson is the headline contribution.
          </p>
        </div>
        <ul className="space-y-2 text-[14.5px] leading-[1.45] text-ink-secondary">
          <li>
            <span className="text-ink">Rubric v3</span> — penalty-only anchors and paired-baseline
            estimation, applied together. Re-score the 50 new framings already inferenced.
          </li>
          <li>
            <span className="text-ink">Independent expert bleed-coding</span> — experts label each
            response yes / no / borderline for "is this response bleed?", rather than scoring it
            with my rubric. That keeps the expert independent of any rubric version I write, so
            the bleed-coded dataset stays a stable validation target even when the rubric evolves.
          </li>
          <li>
            <span className="text-ink">Scenario v2 / v3</span> — vary risk, treatment history, and
            complicating factors so findings do not ride on a single case.
          </li>
          <li>
            <span className="text-ink">Remaining 3 rubrics</span> — social worker, family, patient.
            Phase 1 covers 3 codes; Phase 2 extends to 6.
          </li>
        </ul>
        <div className="border-t border-ink-hairline pt-2.5">
          <div className="text-[11px] font-semibold uppercase tracking-[0.08em] text-ink-muted">
            Out of scope
          </div>
          <p className="mt-1.5 text-[13px] leading-relaxed text-ink-secondary">
            Full expert scoring · multi-turn · jurisdictional variation · Setup A comparison ·
            observational validation against real LLM usage.
          </p>
        </div>
      </div>
    ),
  },

  // 15. APPENDIX — Validation stack + primary sources
  {
    eyebrow: "Appendix",
    title: "Validation stack + primary sources",
    body: (
      <div className="grid grid-cols-2 gap-6">
        <div>
          <div className="mb-2 text-[11px] font-semibold uppercase tracking-[0.08em] text-ink-muted">
            5-layer validation stack
          </div>
          <table className="w-full text-left text-[12.5px]">
            <tbody className="text-ink-secondary">
              <tr className="border-b border-ink-hairline/40">
                <td className="py-2 font-mono text-ink">L1</td>
                <td className="py-2">Pipeline reliability · TRIDENT-consistent ±0.3</td>
                <td className="py-2"><Badge tone="success">VALID</Badge></td>
              </tr>
              <tr className="border-b border-ink-hairline/40">
                <td className="py-2 font-mono text-ink">L2</td>
                <td className="py-2">Judge reliability · κ<sub>human–judge</sub></td>
                <td className="py-2"><Badge tone="info">PILOT</Badge></td>
              </tr>
              <tr className="border-b border-ink-hairline/40">
                <td className="py-2 font-mono text-ink">L3</td>
                <td className="py-2">Rubric validity · expert review</td>
                <td className="py-2"><Badge tone="warning">PHASE 2</Badge></td>
              </tr>
              <tr className="border-b border-ink-hairline/40">
                <td className="py-2 font-mono text-ink">L4</td>
                <td className="py-2">Statistical power · MQ1/SQ1 OK</td>
                <td className="py-2"><Badge tone="warning">PARTIAL</Badge></td>
              </tr>
              <tr>
                <td className="py-2 font-mono text-ink">L5</td>
                <td className="py-2">Construct validity · ICR discriminant</td>
                <td className="py-2"><Badge tone="info">QUEUED</Badge></td>
              </tr>
            </tbody>
          </table>
        </div>
        <div>
          <div className="mb-2 text-[11px] font-semibold uppercase tracking-[0.08em] text-ink-muted">
            Primary sources
          </div>
          <ul className="space-y-1 text-[11.5px] leading-snug text-ink-secondary">
            <li>— Hui et al. 2025 · TRIDENT · arxiv 2507.21134</li>
            <li>— Cheng et al. 2025 · ELEPHANT · arxiv 2505.13995</li>
            <li>— Liang et al. 2025 · clinical role-playing · arxiv 2510.24677</li>
            <li>— Zheng et al. 2023 · MT-Bench / LLM-as-judge · arxiv 2306.05685</li>
            <li>— Panickssery et al. 2024 · self-preference · arxiv 2404.13076</li>
            <li>— Sharma et al. 2023 · sycophancy in language models</li>
            <li>— Wallach et al. 2024 · construct validity in ML eval</li>
            <li>— Flemotomos et al. 2022 · automated CBT fidelity</li>
            <li>— In re K.L., 1 N.Y.3d 362 (2004)</li>
            <li>— NY MHL §9.60 · Kendra's Law</li>
            <li>— Andy Jones · empirical research slides · LessWrong</li>
          </ul>
        </div>
      </div>
    ),
  },
];

function Badge({
  tone,
  children,
}: {
  tone: "success" | "info" | "warning";
  children: React.ReactNode;
}) {
  const palette = {
    success: "bg-status-success/15 text-status-success ring-status-success/30",
    info: "bg-status-info/15 text-status-info ring-status-info/30",
    warning: "bg-status-warning/15 text-status-warning ring-status-warning/30",
  }[tone];
  return (
    <span
      className={clsx(
        "rounded-full px-2 py-0.5 text-[11px] font-semibold ring-1 ring-inset",
        palette,
      )}
    >
      {children}
    </span>
  );
}

export default function SlidesPage() {
  const [index, setIndex] = useState(0);
  const [fullscreen, setFullscreen] = useState(false);

  const total = SLIDES.length;
  const slide = SLIDES[index];

  const goPrev = useCallback(() => setIndex((i) => Math.max(0, i - 1)), []);
  const goNext = useCallback(
    () => setIndex((i) => Math.min(total - 1, i + 1)),
    [total],
  );

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.key === "ArrowLeft" || e.key === "PageUp") {
        e.preventDefault();
        goPrev();
      } else if (
        e.key === "ArrowRight" ||
        e.key === "PageDown" ||
        e.key === " "
      ) {
        e.preventDefault();
        goNext();
      } else if (e.key === "Home") {
        setIndex(0);
      } else if (e.key === "End") {
        setIndex(total - 1);
      } else if (e.key === "f" || e.key === "F") {
        toggleFullscreen();
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [goPrev, goNext, total]);

  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().then(
        () => setFullscreen(true),
        () => {},
      );
    } else {
      document.exitFullscreen().then(
        () => setFullscreen(false),
        () => {},
      );
    }
  }

  const slidesForPrint = useMemo(() => SLIDES, []);

  return (
    <main className="relative flex min-h-screen flex-1 flex-col bg-surface">
      {/* On-screen controls — hidden in print */}
      <div className="no-print sticky top-0 z-10 flex items-center justify-between border-b border-ink-hairline/70 bg-surface/80 px-6 py-3 backdrop-blur">
        <div className="text-[12px] font-semibold uppercase tracking-[0.08em] text-ink-muted">
          CrossSystemEval · Phase 1 Final · Slides
        </div>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={goPrev}
            disabled={index === 0}
            className="inline-flex items-center gap-1 rounded-lg border border-ink-hairline/60 bg-surface-elevated px-3 py-1.5 text-[13px] text-ink-secondary shadow-subtle transition hover:text-ink disabled:opacity-40"
          >
            <ChevronLeft className="h-4 w-4" />
            Prev
          </button>
          <div className="min-w-16 text-center text-[13px] font-mono text-ink-secondary">
            {index + 1} / {total}
          </div>
          <button
            type="button"
            onClick={goNext}
            disabled={index === total - 1}
            className="inline-flex items-center gap-1 rounded-lg border border-ink-hairline/60 bg-surface-elevated px-3 py-1.5 text-[13px] text-ink-secondary shadow-subtle transition hover:text-ink disabled:opacity-40"
          >
            Next
            <ChevronRight className="h-4 w-4" />
          </button>
          <button
            type="button"
            onClick={toggleFullscreen}
            className="ml-2 inline-flex items-center gap-1 rounded-lg border border-ink-hairline/60 bg-surface-elevated px-3 py-1.5 text-[13px] text-ink-secondary shadow-subtle transition hover:text-ink"
            title="Toggle fullscreen (F)"
          >
            {fullscreen ? <Minimize2 className="h-4 w-4" /> : <Maximize2 className="h-4 w-4" />}
            {fullscreen ? "Exit" : "Full"}
          </button>
          <button
            type="button"
            onClick={() => window.print()}
            className="inline-flex items-center gap-1 rounded-lg bg-accent px-3 py-1.5 text-[13px] font-semibold text-white shadow-subtle transition hover:opacity-90"
            title="Save as PDF via system print"
          >
            <Printer className="h-4 w-4" />
            PDF
          </button>
        </div>
      </div>

      {/* On-screen single slide */}
      <div className="no-print flex flex-1 items-center justify-center px-12 py-10">
        <SlideFrame slide={slide} pageNo={index + 1} pageOf={total} />
      </div>

      {/* Print-only: all slides, one per page */}
      <div className="print-only">
        {slidesForPrint.map((s, i) => (
          <div key={i} className="print-slide">
            <SlideFrame slide={s} pageNo={i + 1} pageOf={total} />
          </div>
        ))}
      </div>

      {/* Keyboard hint */}
      <div className="no-print pointer-events-none fixed bottom-4 right-6 text-[11px] text-ink-muted">
        ← → · space · F · Home / End
      </div>

      <style jsx global>{`
        .print-only {
          display: none;
        }
        @media print {
          @page {
            size: 1280px 720px;
            margin: 0;
          }
          aside,
          .no-print {
            display: none !important;
          }
          body {
            background: white !important;
          }
          .print-only {
            display: block;
          }
          .print-slide {
            page-break-after: always;
            page-break-inside: avoid;
            width: 1280px;
            height: 720px;
            padding: 60px 80px;
            box-sizing: border-box;
            display: flex;
            align-items: center;
            justify-content: center;
          }
          .print-slide:last-child {
            page-break-after: auto;
          }
        }
      `}</style>
    </main>
  );
}

function SlideFrame({
  slide,
  pageNo,
  pageOf,
}: {
  slide: Slide;
  pageNo: number;
  pageOf: number;
}) {
  return (
    <article
      className="relative aspect-[16/9] w-full max-w-[1280px] overflow-hidden rounded-2xl bg-surface-elevated p-12 shadow-card ring-1 ring-ink-hairline/40"
      style={{ minHeight: 600 }}
    >
      {slide.eyebrow && (
        <div className="mb-3 text-[12px] font-semibold uppercase tracking-[0.1em] text-accent">
          {slide.eyebrow}
        </div>
      )}
      <h1 className="mb-7 max-w-[26ch] font-display text-[40px] font-semibold leading-[1.08] tracking-tightest text-ink">
        {slide.title}
      </h1>
      <div className="max-w-[60ch]">{slide.body}</div>
      <div className="absolute bottom-5 right-7 text-[11px] font-mono text-ink-muted">
        {pageNo} / {pageOf}
      </div>
    </article>
  );
}
