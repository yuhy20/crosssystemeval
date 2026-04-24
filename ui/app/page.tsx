import { LinkCard, SoftCard, Stat } from "@/components/Card";
import { Page, PageHeader, Section } from "@/components/Container";
import { getLitReviews } from "@/lib/content";

export default function HomePage() {
  const reviews = getLitReviews();
  const paperCount = reviews.reduce((sum, r) => sum + r.papers, 0);

  return (
    <Page>
      <PageHeader
        eyebrow="Benchmark proposal · Sprint Week 1 of 5"
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
            hint="Layer 1 (inference) complete"
          />
          <Stat
            label="Lit reviews"
            value={reviews.length}
            hint={`${paperCount} papers annotated`}
          />
          <Stat
            label="Anchor scenario"
            value="NY MHL §9.60"
            hint="Kendra's Law (Phase 1)"
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
            meta="Week 1 · ~12 hrs logged"
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
            empirical study on NY Kendra's Law (MHL §9.60) demonstrates that
            the instrument produces measurable differentiation across 6
            frontier LLMs.
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
              Framing correction
            </div>
            <p className="mt-2 text-[14.5px] leading-relaxed text-ink-secondary">
              Project reframed from an <em>eval paper</em> to a{" "}
              <em>benchmark proposal paper with pilot empirical study</em>. Primary
              contribution is the methodology (scenario format, rubric-item
              scoring, ICR metric, divergence matrix). Pilot findings demonstrate
              the instrument; they are not the scientific claim.
            </p>
          </SoftCard>
          <SoftCard className="animate-fade-up-delay-3">
            <div className="text-[11px] font-semibold uppercase tracking-[0.08em] text-accent">
              TRIDENT relationship, precisely
            </div>
            <p className="mt-2 text-[14.5px] leading-relaxed text-ink-secondary">
              TRIDENT is the methodological ancestor, not the technical parent.
              We inherit the stance (evaluate AI safety against codified
              professional standards) and the jury architecture; we do not
              inherit pipeline, metric, or failure mode. TRIDENT calibration
              enters the validation stack at Layer 1 only.
            </p>
          </SoftCard>
          <SoftCard className="animate-fade-up-delay-3">
            <div className="text-[11px] font-semibold uppercase tracking-[0.08em] text-accent">
              Jury substitution, defended
            </div>
            <p className="mt-2 text-[14.5px] leading-relaxed text-ink-secondary">
              TRIDENT's original jury (Claude 3.5 Sonnet + Gemma 2-9B) is
              inaccessible on our stack (new-account restriction; Groq
              decommissioning). Substituted with Claude Sonnet 4.6 + Llama 3.1
              8B Instant. Substitution validated at Layer 1 via 6 PASS cells
              across GPT-4o / GPT-4o-mini × law / med / finance.
            </p>
          </SoftCard>
          <SoftCard className="animate-fade-up-delay-3">
            <div className="text-[11px] font-semibold uppercase tracking-[0.08em] text-accent">
              Risk
            </div>
            <p className="mt-2 text-[14.5px] leading-relaxed text-ink-secondary">
              Layers 2 (rubric-item judge reliability) and 5 (construct
              validity) are the load-bearing validation steps and remain
              unexecuted. Sprint weeks 3 and 4 are allocated to them
              respectively. Without Layer 2 evidence, the pilot empirical
              findings in §6.2 cannot be trusted.
            </p>
          </SoftCard>
        </div>
      </Section>
    </Page>
  );
}
