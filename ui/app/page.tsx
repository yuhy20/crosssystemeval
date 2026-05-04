import { LinkCard, SoftCard, Stat } from "@/components/Card";
import { Page, PageHeader, Section } from "@/components/Container";
import { getLitReviews } from "@/lib/content";

export default function HomePage() {
  const reviews = getLitReviews();
  const paperCount = reviews.reduce((sum, r) => sum + r.papers, 0);

  return (
    <Page>
      <PageHeader
        eyebrow="Benchmark proposal · Sprint Week 3 of 5"
        title="CrossSystemEval"
        description="A benchmark methodology for measuring whether LLMs maintain role-appropriate professional-standard fidelity when the same factual scenario is framed from different professional perspectives. Primary contribution is methodological (evaluation unit, rubric-item scoring, Inappropriate Convergence Rate metric); pilot empirical study on NY Kendra's Law is demonstrative."
      />

      <Section>
        <div className="grid grid-cols-2 gap-4 lg:grid-cols-4 animate-fade-up-delay-1">
          <Stat
            label="Sprint end"
            value="May 18"
            hint="5 weeks, ~30 hr budget"
          />
          <Stat
            label="Validation layers"
            value="1 / 5"
            hint="Layer 2 prep — judge rubric pilot live"
          />
          <Stat
            label="Lit reviews"
            value={reviews.length}
            hint={`${paperCount} verified papers`}
          />
          <Stat
            label="Scenario v1"
            value="§9.60"
            hint="Family-petitioner pathway"
          />
        </div>
      </Section>

      <Section title="Navigate">
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-2 animate-fade-up-delay-2">
          <LinkCard
            href="/agenda"
            eyebrow="Primary document"
            title="Research Agenda"
            description="The full benchmark proposal: methodological + substantive research questions, 5-layer validation stack, pilot empirical scope, relationship to TRIDENT and related work."
            meta="Draft v0.3 · reframed as benchmark paper"
            status="draft"
          />
          <LinkCard
            href="/literature"
            eyebrow="Annotated bibliography"
            title="Literature Review"
            description="Gap-oriented reviews bounding the contribution: substantive domain (role eval, authority bias, street-level bureaucracy, mental-health AI) plus methodology (LLM-as-judge validation, rubric construction, construct validity)."
            meta={`${reviews.length} reviews · ${paperCount} papers`}
            status="ready"
          />
          <LinkCard
            href="/worklog"
            eyebrow="Weekly diary"
            title="Worklog"
            description="Decisions, open questions, risks, and changes-of-mind as the sprint progresses. Explicit trail of methodological drift and corrections."
            meta="Week 3 in progress · pilot live, hand-scoring next"
            status="draft"
          />
          <LinkCard
            href="/trident"
            eyebrow="Validation — Layer 1"
            title="Jury Substitution Calibration"
            description="Validates inference pipeline + substitute jury (Claude Sonnet 4.6 + Llama 3.1 8B) against TRIDENT Figure 4 published means. Foundation stone of the 5-layer validation stack — not the full validation."
            meta="6 of 6 PASS · documented substitution"
            status="ready"
          />
          <LinkCard
            href="/pilot"
            eyebrow="Validation — Layer 2 prep"
            title="Rubric Pilot · Judge v1"
            description="Pilot of the 10-item judge rubric (0–3 anchored Likert) on scenario v1, run across 3 cross-family models × 4 prompts (baseline / judge × Q1 / Q2). Tests rubric design — item-correlation, intra-rater κ, baseline-vs-judge delta — before scaling to the remaining roles."
            meta="12 responses generated · awaiting hand-scoring"
            status="draft"
          />
        </div>
      </Section>

      <Section title="Working thesis">
        <SoftCard className="animate-fade-up-delay-3">
          <p className="text-[15.5px] leading-[1.7] text-ink-secondary">
            Every existing AI safety benchmark evaluates model behavior within a{" "}
            <strong className="text-ink">single professional domain</strong>{" "}
            (TRIDENT for law/finance/medicine refusal; PsychiatryBench and
            CounselBench for clinical QA; PAS for police decisions) or measures
            a <strong className="text-ink">single behavioral failure mode</strong>{" "}
            across conditions (ELEPHANT and SycEval for sycophancy). Real-world
            harm occurs at the{" "}
            <strong className="text-ink">boundaries between professional systems</strong>{" "}
            — where standards conflict, where the same facts require
            fundamentally different framings by role. We define a new failure
            mode — <strong className="text-ink">standard bleed</strong>, applying
            one profession's standard in another profession's context given
            identical underlying facts — and propose a measurement methodology:
            an <strong className="text-ink">R × R role-pair divergence matrix</strong>{" "}
            grounded in codified professional standards, with{" "}
            <strong className="text-ink">Inappropriate Convergence Rate (ICR)</strong>{" "}
            as the primary metric. The methodology is the contribution. A pilot
            empirical study on NY Kendra's Law (MHL §9.60) is{" "}
            <strong className="text-ink">scheduled for sprint Weeks 2–4</strong>{" "}
            across a confirmed lineup of 5 frontier LLMs (Claude Sonnet 4.6,
            Claude Haiku 4.5, GPT-4o, GPT-4o-mini, Llama 3.3 70B) plus one
            conditional sixth slot. As of Week 2 mid-sprint, scenario v1
            (family-petitioner pathway) has been drafted with all six role
            analyses, the judge rubric v1 (10 items) is drafted with statute
            traceability, and a 12-cell pilot (3 cross-family models × 4
            prompts) has been generated and is awaiting hand-scoring. Only
            Layer 1 of the 5-layer validation stack (inference pipeline
            calibration against TRIDENT) has been formally validated to date;
            the pilot is the first step toward Layer 2.
          </p>
        </SoftCard>
      </Section>

      <Section title="5-layer validation stack">
        <div className="overflow-hidden rounded-xl bg-surface-elevated shadow-card animate-fade-up-delay-3">
          <table className="w-full text-left text-[14px]">
            <thead className="bg-surface-muted text-[11px] font-semibold uppercase tracking-[0.08em] text-ink-muted">
              <tr>
                <th className="px-5 py-3 w-16">Layer</th>
                <th className="px-5 py-3">Claim</th>
                <th className="px-5 py-3">Status</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-b border-ink-hairline/60">
                <td className="px-5 py-4 font-mono text-[13px] text-ink">1</td>
                <td className="px-5 py-4 text-ink-secondary">Inference pipeline reliability — substitute jury produces TRIDENT-consistent scalar scores within ±0.3.</td>
                <td className="px-5 py-4"><span className="rounded-full bg-status-success/15 px-2 py-0.5 text-[11px] font-semibold text-status-success ring-1 ring-inset ring-status-success/30">VALIDATED</span></td>
              </tr>
              <tr className="border-b border-ink-hairline/60">
                <td className="px-5 py-4 font-mono text-[13px] text-ink">2</td>
                <td className="px-5 py-4 text-ink-secondary">Rubric-item judge reliability — LLM judges can reliably score structured rubric items, κ<sub>human–judge</sub> ≥ 0.6 on a validation subset.</td>
                <td className="px-5 py-4"><span className="rounded-full bg-status-info/15 px-2 py-0.5 text-[11px] font-semibold text-status-info ring-1 ring-inset ring-status-info/30">WEEK 3</span></td>
              </tr>
              <tr className="border-b border-ink-hairline/60">
                <td className="px-5 py-4 font-mono text-[13px] text-ink">3</td>
                <td className="px-5 py-4 text-ink-secondary">Rubric validity — items are source-traceable to statutes and professional codes (full expert review is Phase 2).</td>
                <td className="px-5 py-4"><span className="rounded-full bg-status-warning/15 px-2 py-0.5 text-[11px] font-semibold text-status-warning ring-1 ring-inset ring-status-warning/30">PARTIAL</span></td>
              </tr>
              <tr className="border-b border-ink-hairline/60">
                <td className="px-5 py-4 font-mono text-[13px] text-ink">4</td>
                <td className="px-5 py-4 text-ink-secondary">Statistical power — primary hypothesis adequately powered; exploratory interactions flagged as such.</td>
                <td className="px-5 py-4"><span className="rounded-full bg-status-warning/15 px-2 py-0.5 text-[11px] font-semibold text-status-warning ring-1 ring-inset ring-status-warning/30">PARTIAL</span></td>
              </tr>
              <tr>
                <td className="px-5 py-4 font-mono text-[13px] text-ink">5</td>
                <td className="px-5 py-4 text-ink-secondary">Construct validity — ICR discriminant from sycophancy; pre-registered Pearson r thresholds.</td>
                <td className="px-5 py-4"><span className="rounded-full bg-status-info/15 px-2 py-0.5 text-[11px] font-semibold text-status-info ring-1 ring-inset ring-status-info/30">WEEK 4</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </Section>

      <Section title="What's new this week">
        <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
          <SoftCard className="animate-fade-up-delay-3">
            <div className="text-[11px] font-semibold uppercase tracking-[0.08em] text-accent">
              Judge rubric v1 drafted (10 items, 0–3 anchored)
            </div>
            <p className="mt-2 text-[14.5px] leading-relaxed text-ink-secondary">
              First role rubric written end-to-end with statute traceability:
              7 role-appropriate items (§9.60(c) test, seven prongs, clear-and-
              convincing standard, §9.60(g) procedure, In re K.L. AOT-vs-forced-
              medication, ABA Rule 2.2 impartiality, ABA Rule 2.9 record-bound)
              and 3 bleed-detection items (clinical / advocacy / LLM-use limits).
              Mixed item types are deliberate — the pilot tests whether they
              load on a single factor or stay separable.
            </p>
          </SoftCard>
          <SoftCard className="animate-fade-up-delay-3">
            <div className="text-[11px] font-semibold uppercase tracking-[0.08em] text-accent">
              Pilot pipeline reuses TRIDENT harness
            </div>
            <p className="mt-2 text-[14.5px] leading-relaxed text-ink-secondary">
              Rather than manually pasting prompts into chat windows, the pilot
              extends the TRIDENT calibration harness:{" "}
              <code className="text-ink">build_client</code> factory routes
              <code className="text-ink"> claude-sonnet-4-6</code> (Anthropic),{" "}
              <code className="text-ink">gpt-4o</code> (OpenAI), and{" "}
              <code className="text-ink">llama-3.3-70b-versatile</code> (Groq)
              from the same <code className="text-ink">.env</code>. 12 cells
              (3 models × 4 prompts) generated reproducibly to{" "}
              <code className="text-ink">data/pilot/judge_v1/responses.jsonl</code>{" "}
              with full metadata.
            </p>
          </SoftCard>
          <SoftCard className="animate-fade-up-delay-3">
            <div className="text-[11px] font-semibold uppercase tracking-[0.08em] text-accent">
              ICR pre-registered as delta-from-baseline
            </div>
            <p className="mt-2 text-[14.5px] leading-relaxed text-ink-secondary">
              Research agenda §5.4 commits to computing ICR as the delta between
              role-framed and no-claim-baseline scores per item, not as
              absolute role-framed scores. This separates{" "}
              <strong className="text-ink">standard bleed</strong> (the role
              claim moves the model in an inappropriate direction) from{" "}
              <strong className="text-ink">knowledge gap</strong> (the model
              can't apply the standard regardless of who's asking). The pilot's
              baseline-vs-judge-framed delta operationalizes this for one role.
            </p>
          </SoftCard>
          <SoftCard className="animate-fade-up-delay-3">
            <div className="text-[11px] font-semibold uppercase tracking-[0.08em] text-accent">
              Risk · Week 2 slippage
            </div>
            <p className="mt-2 text-[14.5px] leading-relaxed text-ink-secondary">
              Hand-scoring the 12 responses (≥24h between sessions) and the
              §9.60 direct-statute verification both slipped from Week 2. Both
              moved to early Week 3 — neither blocks scaling, but both must
              clear before the rubric is extended to therapist (planned
              second-role pilot). Layers 2 and 5 of the validation stack remain
              unexecuted; Weeks 3 and 4 still allocated to them.
            </p>
          </SoftCard>
        </div>
      </Section>
    </Page>
  );
}
