import Link from "next/link";
import { Page, PageHeader } from "@/components/Container";

export default function NotFound() {
  return (
    <Page>
      <PageHeader
        eyebrow="404"
        title="Not found"
        description="This route does not exist yet — it may be planned for a future sprint week."
      />
      <Link
        href="/"
        className="text-[14px] font-medium text-accent hover:underline"
      >
        ← Back to overview
      </Link>
    </Page>
  );
}
