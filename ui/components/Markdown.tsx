import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function Markdown({ children }: { children: string }) {
  return (
    <article className="prose prose-neutral max-w-none prose-headings:font-display prose-headings:tracking-tight prose-h1:text-[32px] prose-h2:mt-10 prose-h2:text-[22px] prose-h3:text-[17px] prose-p:text-[15.5px] prose-p:leading-[1.65] prose-li:text-[15.5px] prose-li:leading-[1.65] prose-strong:text-ink prose-a:text-accent prose-a:no-underline hover:prose-a:underline prose-hr:border-ink-faint/60">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{children}</ReactMarkdown>
    </article>
  );
}
