import Link from "next/link";
import { ChevronLeft } from "lucide-react";
import { Page, PageHeader, Section } from "@/components/Container";
import { SoftCard, Stat } from "@/components/Card";
import Markdown from "@/components/Markdown";
import { getLlmJudgeAnalysis } from "@/lib/content";

export default function LlmJudgePage() {
  const analysis = getLlmJudgeAnalysis();

  return (
    <Page>
      <Link
        href="/pilot"
        className="mb-10 inline-flex items-center gap-1 text-[13px] font-medium text-ink-muted transition-colors hover:text-ink"
      >
        <ChevronLeft className="h-4 w-4" strokeWidth={2} />
        Rubric pilot
      </Link>

      <PageHeader
        eyebrow="Validation Stack · Layer 2 — LLM-judge layer"
        title="LLM-as-judge analysis"
        description="Two cross-family judges (Claude Sonnet 4.6 + GPT-4o) score every pilot response on the 10-item judge rubric. Randomized item presentation order per call, temperature 0, JSON output. Treated as a directional pilot signal — NOT a validation result. The validated κ_human–judge number comes from the lawyer's scoring."
      />

      <Section>
        <div className="grid grid-cols-2 gap-4 lg:grid-cols-4 animate-fade-up-delay-1">
          <Stat
            label="Responses scored"
            value={String(analysis.nResponses || "—")}
            hint="5 models × 4 prompts"
          />
          <Stat label="Judges" value="2" hint="Claude · GPT" />
          <Stat
            label="Judge calls"
            value={String(analysis.nJudgeCalls || "—")}
            hint="responses × judges"
          />
          <Stat
            label="Status"
            value={analysis.exists ? "Generated" : "Pending"}
            hint={analysis.generatedAt ?? "run pipeline"}
          />
        </div>
      </Section>

      <Section title="What this analysis is and is not">
        <SoftCard className="animate-fade-up-delay-2">
          <ul className="space-y-2 text-[14.5px] leading-relaxed text-ink-secondary">
            <li>
              <span className="font-medium text-ink">Is:</span> a directional
              pilot signal — does the role-claim manipulation move scores, do
              models default toward judge-appropriate content unprompted, do
              the two judges agree on the rubric items, is there a length
              confound, is there a self-preference floor.
            </li>
            <li>
              <span className="font-medium text-ink">Is not:</span> a
              validated Layer 2 result. The pre-registered Phase 1 threshold
              is κ_human–judge ≥ 0.6 against an expert rater, not κ_LLM–LLM.
              The lawyer-scoring packet is in flight.
            </li>
            <li>
              <span className="font-medium text-ink">Method anchors:</span>{" "}
              Zheng et al. 2306.05685 (MT-Bench, dual judges), Wang et al.
              (position-bias mitigation via randomized item order),
              Panickssery 2404.13076 (self-preference floor check), Cohen κ
              (descriptive only — 2 judges is not sufficient for a defensible
              agreement claim).
            </li>
          </ul>
        </SoftCard>
      </Section>

      {analysis.exists ? (
        <Section title="Analysis">
          <SoftCard className="animate-fade-up-delay-3">
            <Markdown>{analysis.markdown}</Markdown>
          </SoftCard>
        </Section>
      ) : (
        <Section title="Run the pipeline">
          <SoftCard className="animate-fade-up-delay-3">
            <p className="text-[14.5px] leading-relaxed text-ink-secondary">
              No analysis file yet. To generate it:
            </p>
            <pre className="mt-4 overflow-x-auto rounded-lg bg-surface-muted p-4 text-[12.5px] leading-relaxed text-ink">
              <code>{`cd code/trident_repro
uv run python scripts/run_llm_judge.py
uv run python scripts/analyze_llm_judge.py`}</code>
            </pre>
            <p className="mt-4 text-[13px] text-ink-muted">
              Outputs land at{" "}
              <code className="rounded bg-surface-muted px-1 py-0.5">
                data/pilot/judge_v2/llm_judge_analysis.md
              </code>{" "}
              and the JSON sibling. Refresh this page after the analysis
              script completes.
            </p>
          </SoftCard>
        </Section>
      )}
    </Page>
  );
}
