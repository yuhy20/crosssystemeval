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
        description="Gap-oriented reviews bounding the contribution. The substantive domain reviews (authority bias, role-conditioned eval, Lipsky × AI, mental-health AI) justify why the benchmark is needed. The methodology review (LLM-as-judge validation, rubric construction psychometrics, construct validity) justifies that the methodology is constructed defensibly. Each entry includes a specific claim about relevance — not a general summary."
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
