import { Page, PageHeader } from "@/components/Container";
import Markdown from "@/components/Markdown";
import { getResearchAgenda } from "@/lib/content";

export default function AgendaPage() {
  const { content, updated } = getResearchAgenda();

  return (
    <Page>
      <PageHeader
        eyebrow={`Updated ${updated}`}
        title="Research Agenda"
        description="Primary research document. Motivates the project, states hypotheses with pre-registered analyses, specifies methodology, and scopes the 5-week sprint against deferred Phase 2 work."
      />

      <div className="animate-fade-up-delay-1 max-w-prose">
        <Markdown>{content}</Markdown>
      </div>
    </Page>
  );
}
