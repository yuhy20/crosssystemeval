import { LinkCard, SoftCard } from "@/components/Card";
import { Page, PageHeader, Section } from "@/components/Container";
import { getOutreachDocs, OutreachDocMeta } from "@/lib/content";

const groupOrder: Array<{
  key: OutreachDocMeta["group"];
  title: string;
  description: string;
}> = [
  {
    key: "index",
    title: "Start here",
    description:
      "Overview of the outreach packet set and the pre-flight checklist that must be settled before anything goes to a human.",
  },
  {
    key: "shared",
    title: "Shared",
    description:
      "Resolve once, apply to both engagements. Bracketed template; fill in before sending either brief.",
  },
  {
    key: "lawyer",
    title: "Lawyer — judge-rubric expert validation",
    description:
      "Send 1–2 days before scoring. Brief is one-page framing; scoring packet converts to a Google Doc the lawyer fills in.",
  },
  {
    key: "tasc",
    title: "TASC employee — LCSW-role consultation",
    description:
      "Three-step protocol: async pre-flight first, then brief if pre-flight clears, then a 60-min call run from the internal call guide (not sent).",
  },
];

const statusFor = (
  status: string,
): "ready" | "draft" | "blocked" | "pending" => {
  if (status.toLowerCase().includes("ready")) return "ready";
  if (status.toLowerCase().includes("blocked")) return "blocked";
  if (status.toLowerCase().includes("pending")) return "pending";
  return "draft";
};

export default function OutreachPage() {
  const docs = getOutreachDocs();

  return (
    <Page>
      <PageHeader
        eyebrow="Phase 1 · Expert reviewer outreach"
        title="Outreach packets"
        description="Plain-language artifacts for two expert engagements supporting the judge-rubric pilot: a NY MHL §9.60 lawyer (rubric expert validation) and a NY TASC employee (LCSW case-management consultation). All drafts. Manual review required before anything is sent — both helpers' first impression is load-bearing."
      />

      <Section title="Pre-flight checklist">
        <SoftCard className="animate-fade-up-delay-1">
          <ul className="space-y-2 text-[14.5px] leading-relaxed text-ink-secondary">
            <li>
              <span className="font-medium text-ink">Authorship policy filled in</span>{" "}
              — at minimum, decide acknowledgement-only, paid consultant, or
              coauthor for each helper. Same policy block goes into both briefs.
            </li>
            <li>
              <span className="font-medium text-ink">§9.60 statute verified</span>{" "}
              — at least the items the rubric cites (§9.60(c), §9.60(g))
              against the codified NY text, not a summary source.
            </li>
            <li>
              <span className="font-medium text-ink">
                Marcus-Johnson plan-authorship question resolved
              </span>{" "}
              — or staged as the first fact-check in the TASC pre-flight.
            </li>
          </ul>
          <p className="mt-4 text-[13px] leading-relaxed text-ink-muted">
            If any packet feels off — wrong framing, too long, jargon-heavy,
            wastes the helper&apos;s time — flag it before sending. Iteration is
            cheap; a botched first contact is not.
          </p>
        </SoftCard>
      </Section>

      {groupOrder.map((group) => {
        const groupDocs = docs.filter((d) => d.group === group.key);
        if (groupDocs.length === 0) return null;
        return (
          <Section key={group.key} title={group.title}>
            <p className="mb-5 max-w-prose text-[14px] leading-relaxed text-ink-secondary animate-fade-up-delay-2">
              {group.description}
            </p>
            <div className="grid grid-cols-1 gap-3 md:grid-cols-2 animate-fade-up-delay-3">
              {groupDocs.map((doc) => (
                <LinkCard
                  key={doc.slug}
                  href={`/outreach/${doc.slug}`}
                  eyebrow={doc.filename}
                  title={doc.title || doc.slug}
                  description={doc.purpose}
                  meta={
                    [doc.recipient, doc.length].filter(Boolean).join(" · ") ||
                    undefined
                  }
                  status={statusFor(doc.status)}
                />
              ))}
            </div>
          </Section>
        );
      })}
    </Page>
  );
}
