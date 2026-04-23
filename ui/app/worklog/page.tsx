import { Page, PageHeader, Section } from "@/components/Container";
import { SoftCard } from "@/components/Card";
import Markdown from "@/components/Markdown";
import { getWorklogs } from "@/lib/content";

export default function WorklogPage() {
  const logs = getWorklogs();

  return (
    <Page>
      <PageHeader
        eyebrow="Weekly diary"
        title="Worklog"
        description="Decisions, open questions, and risks tracked week by week. Updated as the sprint progresses; includes changes-of-mind and reasons, not just status."
      />

      <Section>
        <div className="flex flex-col gap-8 animate-fade-up-delay-1">
          {logs.map((log) => (
            <div key={log.filename}>
              <div className="mb-4 flex items-baseline gap-3">
                <div className="font-display text-[22px] font-semibold tracking-tighter text-ink">
                  Week {log.week}
                </div>
                <div className="text-[13px] text-ink-muted">{log.dates}</div>
              </div>
              <SoftCard>
                <Markdown>{log.content}</Markdown>
              </SoftCard>
            </div>
          ))}
        </div>
      </Section>
    </Page>
  );
}
