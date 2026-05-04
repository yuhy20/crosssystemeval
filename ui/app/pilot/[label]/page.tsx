import Link from "next/link";
import { notFound } from "next/navigation";
import { ChevronLeft } from "lucide-react";
import Markdown from "@/components/Markdown";
import { Page } from "@/components/Container";
import { getPilotData, getPilotSheet } from "@/lib/content";

export function generateStaticParams() {
  return getPilotData().responses.map((r) => ({ label: r.label }));
}

export default function PilotResponsePage({
  params,
}: {
  params: { label: string };
}) {
  const sheet = getPilotSheet(params.label);
  if (!sheet) notFound();

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
          <span>{sheet.label.replace("_", " · ")}</span>
          <span className="h-1 w-1 rounded-full bg-ink-muted/50" />
          <span className="text-ink-muted">Session 1 shuffle · blind to model</span>
        </div>
        <h1 className="font-display text-[36px] font-semibold leading-[1.08] tracking-tightest text-ink">
          Anonymized response
        </h1>
        <p className="mt-3 max-w-prose text-[14.5px] leading-relaxed text-ink-secondary">
          Hand-score in the local markdown file at{" "}
          <code className="rounded bg-surface-muted px-1.5 py-0.5 text-[13px] text-ink">
            data/pilot/judge_v1/scoring_session_1/{sheet.label}.md
          </code>
          . Model and prompt-id are intentionally hidden from this view; they
          live only in <code className="text-ink">SCORING_KEY.md</code> and
          should not be opened until both scoring sessions are complete.
        </p>
      </header>

      <div className="animate-fade-up-delay-1">
        <Markdown>{sheet.sheetMarkdown}</Markdown>
      </div>
    </Page>
  );
}
