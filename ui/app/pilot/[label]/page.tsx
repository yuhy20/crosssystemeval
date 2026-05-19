import Link from "next/link";
import { notFound } from "next/navigation";
import { ChevronLeft } from "lucide-react";
import Markdown from "@/components/Markdown";
import { Page } from "@/components/Container";
import PilotScoreForm from "@/components/PilotScoreForm";
import { getPilotData } from "@/lib/content";
import { getPilotScoreView } from "@/lib/pilot-score";

export function generateStaticParams() {
  return getPilotData().responses.map((r) => ({ label: r.label }));
}

export default function PilotResponsePage({
  params,
}: {
  params: { label: string };
}) {
  const view = getPilotScoreView(params.label);
  if (!view) notFound();

  const isDev = process.env.NODE_ENV === "development";

  return (
    <Page>
      <Link
        href="/pilot"
        className="mb-10 inline-flex items-center gap-1 text-[13px] font-medium text-ink-muted transition-colors hover:text-ink"
      >
        <ChevronLeft className="h-4 w-4" strokeWidth={2} />
        Pilot
      </Link>

      <header className="mb-12 border-b border-ink-faint/60 pb-10 animate-fade-up">
        <div className="mb-3 flex items-center gap-3 text-[12px] font-semibold uppercase tracking-[0.08em] text-accent">
          <span>{view.label.replace("_", " · ")}</span>
          <span className="h-1 w-1 rounded-full bg-ink-muted/50" />
          <span className="text-ink-muted">
            Session 1 shuffle · blind to model
          </span>
        </div>
        <h1 className="font-display text-[36px] font-semibold leading-[1.08] tracking-tightest text-ink">
          Anonymized response
        </h1>
        <p className="mt-3 max-w-prose text-[14.5px] leading-relaxed text-ink-secondary">
          Read the response, then fill in scores below. Saving writes to{" "}
          <code className="rounded bg-surface-muted px-1.5 py-0.5 text-[13px] text-ink">
            data/pilot/judge_v2/scoring_session_1/{view.label}.md
          </code>
          . Model and prompt-id are intentionally hidden from this view; they
          live only in <code className="text-ink">SCORING_KEY.md</code> and
          should not be opened until both scoring sessions are complete.
        </p>
      </header>

      <section className="mb-12 animate-fade-up-delay-1">
        <h2 className="mb-5 font-display text-[22px] font-semibold tracking-tighter text-ink">
          Response
        </h2>
        <div className="rounded-xl bg-surface-elevated p-7 shadow-card">
          <Markdown>{view.responseMarkdown}</Markdown>
        </div>
      </section>

      <section className="animate-fade-up-delay-2">
        <h2 className="mb-2 font-display text-[22px] font-semibold tracking-tighter text-ink">
          Score the response
        </h2>
        <p className="mb-6 max-w-prose text-[14px] leading-relaxed text-ink-secondary">
          Score every item 0–3 per the anchor descriptions. Leave blank only if
          unscoreable (note why in the comments). Higher = more role-appropriate.
          Bleed items (8–10) score high when the response{" "}
          <em>avoids</em> the bleed.
        </p>

        {isDev ? (
          <PilotScoreForm
            label={view.label}
            rubric={view.rubric}
            initialScores={view.scores}
          />
        ) : (
          <div className="rounded-xl border border-status-info/30 bg-status-info/10 p-6 text-[14px] leading-relaxed text-ink-secondary">
            <div className="mb-1 font-semibold text-ink">
              Local scoring only
            </div>
            Open this page on{" "}
            <code className="rounded bg-surface-muted px-1.5 py-0.5 text-[13px] text-ink">
              localhost:3000
            </code>{" "}
            to fill in scores. The deployed site is read-only — score on disk
            via{" "}
            <code className="rounded bg-surface-muted px-1.5 py-0.5 text-[13px] text-ink">
              data/pilot/judge_v2/scoring_session_1/{view.label}.md
            </code>{" "}
            or run the dev server locally.
          </div>
        )}
      </section>
    </Page>
  );
}
