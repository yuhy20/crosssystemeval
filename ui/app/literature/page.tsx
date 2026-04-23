import { LinkCard } from "@/components/Card";
import { Page, PageHeader, Section } from "@/components/Container";
import { getLitReviews } from "@/lib/content";

export default function LiteraturePage() {
  const reviews = getLitReviews();

  return (
    <Page>
      <PageHeader
        eyebrow="Annotated bibliography"
        title="Literature Review"
        description="Four gap-oriented reviews covering the intellectual territory CrossSystemEval sits in. Each annotated entry includes methodology, key finding, and a specific claim about relevance to the current project — not a general summary."
      />

      <Section>
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-2 animate-fade-up-delay-1">
          {reviews.map((r) => (
            <LinkCard
              key={r.slug}
              href={`/literature/${r.slug}`}
              eyebrow={`${r.papers} papers`}
              title={r.title}
              description={r.subtitle}
              meta={`Synthesized · ${r.date}`}
              status="ready"
            />
          ))}
        </div>
      </Section>
    </Page>
  );
}
