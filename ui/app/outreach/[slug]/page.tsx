import Link from "next/link";
import { notFound } from "next/navigation";
import { ChevronLeft } from "lucide-react";
import Markdown from "@/components/Markdown";
import { SoftCard } from "@/components/Card";
import { Page } from "@/components/Container";
import { getOutreachDoc, getOutreachDocs } from "@/lib/content";

export function generateStaticParams() {
  return getOutreachDocs().map((d) => ({ slug: d.slug }));
}

export default function OutreachDocPage({
  params,
}: {
  params: { slug: string };
}) {
  const doc = getOutreachDoc(params.slug);
  if (!doc) notFound();

  const metaRows: Array<{ label: string; value: string }> = [
    { label: "Recipient", value: doc.recipient },
    { label: "Length", value: doc.length },
    { label: "Status", value: doc.status },
    { label: "Date", value: doc.date },
    { label: "File", value: `outreach/${doc.filename}` },
  ].filter((r) => r.value);

  return (
    <Page>
      <Link
        href="/outreach"
        className="mb-10 inline-flex items-center gap-1 text-[13px] font-medium text-ink-muted transition-colors hover:text-ink"
      >
        <ChevronLeft className="h-4 w-4" strokeWidth={2} />
        Outreach
      </Link>

      <header className="mb-10 border-b border-ink-faint/60 pb-10 animate-fade-up">
        <div className="mb-3 text-[12px] font-semibold uppercase tracking-[0.08em] text-accent">
          {doc.filename}
        </div>
        <h1 className="font-display text-[36px] font-semibold leading-[1.08] tracking-tightest text-ink">
          {doc.title || doc.slug}
        </h1>
        {doc.purpose && (
          <p className="mt-3 max-w-prose text-[14.5px] leading-relaxed text-ink-secondary">
            {doc.purpose}
          </p>
        )}
      </header>

      {metaRows.length > 0 && (
        <div className="mb-10 animate-fade-up-delay-1">
          <SoftCard>
            <dl className="grid grid-cols-1 gap-x-8 gap-y-3 sm:grid-cols-2">
              {metaRows.map((row) => (
                <div
                  key={row.label}
                  className="flex flex-col gap-0.5 text-[13.5px]"
                >
                  <dt className="text-[11px] font-semibold uppercase tracking-[0.08em] text-ink-muted">
                    {row.label}
                  </dt>
                  <dd className="text-ink-secondary">{row.value}</dd>
                </div>
              ))}
            </dl>
          </SoftCard>
        </div>
      )}

      <div className="animate-fade-up-delay-2">
        <Markdown>{doc.content}</Markdown>
      </div>
    </Page>
  );
}
