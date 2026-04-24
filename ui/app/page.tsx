import { LinkCard, SoftCard, Stat } from "@/components/Card";
import { Page, PageHeader, Section } from "@/components/Container";
import { getLitReviews } from "@/lib/content";

export default function HomePage() {
  const reviews = getLitReviews();
  const paperCount = reviews.reduce((sum, r) => sum + r.papers, 0);

  return (
    <Page>
      <PageHeader
        eyebrow="Sprint Week 1 of 5"
        title="CrossSystemEval"
        description="Measuring whether LLMs maintain role-appropriate professional standards when the same factual situation is framed from different professional perspectives — and whether that failure is structurally distinct from sycophancy."
      />

      <Section>
        <div className="grid grid-cols-2 gap-4 lg:grid-cols-4 animate-fade-up-delay-1">
          <Stat
            label="Sprint end"
            value="May 18"
            hint="5 weeks, ~30 hr budget"
          />
          <Stat
            label="Lit reviews"
            value={reviews.length}
            hint={`${paperCount} papers annotated`}
          />
          <Stat
            label="Models tested"
            value="6+2"
            hint="Factorial provider × size"
          />
          <Stat
            label="Anchor scenario"
            value="NY MHL"
            hint="Kendra's Law & §9.39"
          />
        </div>
      </Section>

      <Section title="Navigate">
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-2 animate-fade-up-delay-2">
          <LinkCard
            href="/agenda"
            eyebrow="Primary document"
            title="Research Agenda"
            description="Motivation, hypotheses, methodology, pre-registered analyses, timeline. Updated with literature integration and model lineup."
            meta="Draft v0.2 · ~2,800 words"
            status="draft"
          />
          <LinkCard
            href="/literature"
            eyebrow="Annotated bibliography"
            title="Literature Review"
            description="Four gap-oriented reviews covering the intersection of role-based evaluation, authority bias, street-level bureaucracy, and mental-health AI."
            meta={`${reviews.length} reviews · ${paperCount} papers`}
            status="ready"
          />
          <LinkCard
            href="/worklog"
            eyebrow="Weekly diary"
            title="Worklog"
            description="Decisions, open questions, risks, and changes-of-mind as the sprint progresses."
            meta="Week 1 · ~8 hrs logged"
            status="draft"
          />
          <LinkCard
            href="/trident"
            eyebrow="Calibration"
            title="TRIDENT Calibration"
            description="Pipeline validated against TRIDENT Figure 4 on GPT-4o + GPT-4o-mini × 3 domains with a documented substitute jury (Claude Sonnet 4.6 + Llama 3.1 8B). 6 of 6 PASS within ±0.3 tolerance."
            meta="6 / 6 PASS · 18 files · 36 tests"
            status="ready"
          />
        </div>
      </Section>

      <Section title="Working thesis">
        <SoftCard className="animate-fade-up-delay-3">
          <p className="text-[15.5px] leading-[1.7] text-ink-secondary">
            Every existing AI safety benchmark evaluates model behavior within a{" "}
            <strong className="text-ink">single domain</strong> (TRIDENT,
            PsychiatryBench, PAS) or measures a{" "}
            <strong className="text-ink">single failure mode</strong> (ELEPHANT,
            SycEval). Real-world harm happens at the{" "}
            <strong className="text-ink">boundaries</strong> between
            professional systems — where standards conflict, where the same
            facts require fundamentally different framings. We introduce a new
            failure mode:{" "}
            <strong className="text-ink">standard bleed</strong>, when a model
            applies one profession's standard in another profession's context
            given identical underlying facts. We operationalize it using an{" "}
            <strong className="text-ink">R × R role divergence matrix</strong>{" "}
            grounded in codified professional standards, anchored to
            involuntary psychiatric commitment under NY Mental Hygiene Law.
          </p>
        </SoftCard>
      </Section>

      <Section title="What's new this week">
        <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
          <SoftCard className="animate-fade-up-delay-3">
            <div className="text-[11px] font-semibold uppercase tracking-[0.08em] text-accent">
              Finding
            </div>
            <p className="mt-2 text-[14.5px] leading-relaxed text-ink-secondary">
              No existing benchmark combines (a) user-professional-role axis,
              (b) cross-domain invariance testing, and (c) explicit normative
              expected-divergence matrix. Closest prior: Wagner et al.
              (mandated-reporter role variation) and U-SafeBench (query × user
              × response cell structure).
            </p>
          </SoftCard>
          <SoftCard className="animate-fade-up-delay-3">
            <div className="text-[11px] font-semibold uppercase tracking-[0.08em] text-accent">
              Decision
            </div>
            <p className="mt-2 text-[14.5px] leading-relaxed text-ink-secondary">
              Model count revised from 3 to 6 primary + 2 exploratory.
              Factorial provider × size design (Anthropic, OpenAI, Google,
              Meta) plus Meditron-vs-Llama for the specialization hypothesis
              (H4). Within sprint budget at ~$5–22 API cost.
            </p>
          </SoftCard>
          <SoftCard className="animate-fade-up-delay-3">
            <div className="text-[11px] font-semibold uppercase tracking-[0.08em] text-accent">
              Risk
            </div>
            <p className="mt-2 text-[14.5px] leading-relaxed text-ink-secondary">
              Liang et al. (Oct 2025) mechanistically show models don't
              internally represent user authority. Null-hypothesis threat for
              exploratory H5 — requires distinguishing surface linguistic
              change from normative-standard application in the rubric.
            </p>
          </SoftCard>
          <SoftCard className="animate-fade-up-delay-3">
            <div className="text-[11px] font-semibold uppercase tracking-[0.08em] text-accent">
              Risk
            </div>
            <p className="mt-2 text-[14.5px] leading-relaxed text-ink-secondary">
              Chen et al. (Aug 2025): models sanitize danger cues in role-play
              even when explicitly prompted — a safety-training artifact that
              could undermine commitment-scenario fidelity. Mitigation may
              require adversarial / red-team prompt variants.
            </p>
          </SoftCard>
        </div>
      </Section>
    </Page>
  );
}
