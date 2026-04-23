import Link from "next/link";
import { notFound } from "next/navigation";
import { ChevronLeft } from "lucide-react";
import Markdown from "@/components/Markdown";
import { Page } from "@/components/Container";
import { getLitReview, getLitReviews } from "@/lib/content";

export function generateStaticParams() {
  return getLitReviews().map((r) => ({ slug: r.slug }));
}

export default function LitReviewDetail({
  params,
}: {
  params: { slug: string };
}) {
  const review = getLitReview(params.slug);
  if (!review) notFound();

  return (
    <Page>
      <Link
        href="/literature"
        className="mb-10 inline-flex items-center gap-1 text-[13px] font-medium text-ink-muted transition-colors hover:text-ink"
      >
        <ChevronLeft className="h-4 w-4" strokeWidth={2} />
        Literature
      </Link>

      <header className="mb-12 border-b border-ink-faint/60 pb-10 animate-fade-up">
        <div className="mb-3 flex items-center gap-3 text-[12px] font-semibold uppercase tracking-[0.08em] text-accent">
          <span>{review.papers} papers</span>
          <span className="h-1 w-1 rounded-full bg-ink-muted/50" />
          <span className="text-ink-muted">Synthesized {review.date}</span>
        </div>
        <h1 className="font-display text-[42px] font-semibold leading-[1.08] tracking-tightest text-ink">
          {review.title}
        </h1>
        <p className="mt-4 max-w-prose text-[17px] leading-relaxed text-ink-secondary">
          {review.subtitle}
        </p>
      </header>

      <div className="animate-fade-up-delay-1">
        <Markdown>{review.content}</Markdown>
      </div>
    </Page>
  );
}
