import { Page, PageHeader } from "@/components/Container";
import Markdown from "@/components/Markdown";
import { getResearchAgenda } from "@/lib/content";

export default function AgendaPage() {
  const { content, updated } = getResearchAgenda();

  return (
    <Page>
      <PageHeader
        eyebrow={`Benchmark proposal · updated ${updated}`}
        title="Research Agenda"
        description="The primary document. Frames the project as a benchmark proposal paper with pilot empirical study, specifies the 5-layer validation stack, documents the jury substitution from TRIDENT, and defines the scope of what the sprint claims vs. what is deferred to Phase 2."
      />

      <div className="animate-fade-up-delay-1 max-w-prose">
        <Markdown>{content}</Markdown>
      </div>
    </Page>
  );
}
