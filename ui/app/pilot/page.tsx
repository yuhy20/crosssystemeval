import { LinkCard, SoftCard, Stat } from "@/components/Card";
import { Page, PageHeader, Section } from "@/components/Container";
import Markdown from "@/components/Markdown";
import { getPilotData } from "@/lib/content";

export default function PilotPage() {
  const data = getPilotData();
  const totalCells = data.responses.length;

  return (
    <Page>
      <PageHeader
        eyebrow="Validation Stack · Layer 2 prep · Judge Rubric v1"
        title="Rubric pilot — judge framing"
        description="Pilot of the judge rubric (10 items, 0–3 anchored Likert) on scenario v1, run across 3 cross-family models × 4 prompts (baseline / judge × Q1 risk-frame / Q2 neutral-frame). The pilot tests the rubric design — item-correlation matrix, intra-rater κ, and baseline-vs-judge-framed delta — before scaling to the remaining five roles. Hand-scored across two sessions ≥24h apart, blind to prompt-id at session level."
      />

      <Section>
        <div className="grid grid-cols-2 gap-4 lg:grid-cols-4 animate-fade-up-delay-1">
          <Stat label="Models" value="3" hint="Claude · GPT · Llama" />
          <Stat label="Prompts" value="4" hint="2 framings × 2 questions" />
          <Stat label="Cells" value={String(totalCells)} hint="all completed naturally" />
          <Stat label="Items" value="10" hint="7 role-appropriate · 3 bleed" />
        </div>
      </Section>

      <Section title="How to score (workflow)">
        <SoftCard className="animate-fade-up-delay-2">
          <ol className="ml-5 list-decimal space-y-2 text-[14.5px] leading-relaxed text-ink-secondary">
            <li>
              Click into each anonymized response below in the order shown
              (session-1 shuffle). Read the response, then score every item
              0–3 in the local markdown sheet at{" "}
              <code className="rounded bg-surface-muted px-1.5 py-0.5 text-[12.5px] text-ink">
                data/pilot/judge_v1/scoring_session_1/response_NN.md
              </code>
              .
            </li>
            <li>
              ≥24h later, re-score from a freshly shuffled set at{" "}
              <code className="rounded bg-surface-muted px-1.5 py-0.5 text-[12.5px] text-ink">
                scoring_session_2/
              </code>
              . Do not re-read your session-1 scores — the test-retest design
              depends on session 2 being a re-score, not a re-confirmation.
            </li>
            <li>
              After both sessions, open{" "}
              <code className="rounded bg-surface-muted px-1.5 py-0.5 text-[12.5px] text-ink">
                SCORING_KEY.md
              </code>{" "}
              in each session directory and run the analysis (item-correlation
              matrix, intra-rater κ per item, baseline-vs-judge delta). Decision
              gates documented in the rubric itself.
            </li>
          </ol>
          <p className="mt-4 text-[13px] leading-relaxed text-ink-muted">
            The UI intentionally does not surface model identity per response —
            that lives only in <code>SCORING_KEY.md</code> on disk. This keeps
            navigating from the UI compatible with the blind protocol.
          </p>
        </SoftCard>
      </Section>

      <Section title={`Responses (${totalCells} · session-1 shuffle)`}>
        <div className="grid grid-cols-1 gap-3 md:grid-cols-2 lg:grid-cols-3 animate-fade-up-delay-3">
          {data.responses.map((r) => (
            <LinkCard
              key={r.label}
              href={`/pilot/${r.label}`}
              eyebrow={r.label.replace("_", " · ")}
              title={`Anonymized response`}
              description={`A response to scenario v1 (Maya Chen / §9.60 hearing). Model and prompt-id intentionally hidden from the UI — score blind first, then check SCORING_KEY.md after both sessions.`}
              meta={`${r.charCount.toLocaleString()} chars`}
              status="draft"
            />
          ))}
        </div>
      </Section>

      <Section title="The 4 prompts (shared across all 3 models)">
        <SoftCard className="animate-fade-up-delay-3">
          <div className="prose prose-neutral max-w-none prose-headings:font-display prose-h3:text-[15px] prose-p:text-[14.5px] prose-li:text-[14.5px]">
            <Markdown>{data.promptsMarkdown}</Markdown>
          </div>
        </SoftCard>
      </Section>

      <Section title="Rubric — Judge v1 (10 items, 0–3 anchored)">
        <SoftCard className="animate-fade-up-delay-3">
          <Markdown>{data.rubricMarkdown}</Markdown>
        </SoftCard>
      </Section>

      <Section title="Scoring sheet template">
        <SoftCard className="animate-fade-up-delay-3">
          <Markdown>{data.scoringSheetTemplate}</Markdown>
        </SoftCard>
      </Section>
    </Page>
  );
}
