import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";

const ROOT = path.resolve(process.cwd(), "..");

export interface LitReviewMeta {
  slug: string;
  title: string;
  subtitle: string;
  papers: number;
  status: string;
  date: string;
  filename: string;
}

export interface LitReview extends LitReviewMeta {
  content: string;
}

export function getLitReviews(): LitReviewMeta[] {
  const dir = path.join(ROOT, "lit_review");
  if (!fs.existsSync(dir)) return [];

  const files = fs
    .readdirSync(dir)
    .filter((f) => f.endsWith(".md"))
    .sort();

  return files.map((filename) => {
    const raw = fs.readFileSync(path.join(dir, filename), "utf8");
    const { data } = matter(raw);
    return {
      slug: data.slug,
      title: data.title,
      subtitle: data.subtitle,
      papers: data.papers ?? 0,
      status: data.status ?? "draft",
      date: data.date ?? "",
      filename,
    };
  });
}

export function getLitReview(slug: string): LitReview | null {
  const reviews = getLitReviews();
  const meta = reviews.find((r) => r.slug === slug);
  if (!meta) return null;

  const raw = fs.readFileSync(
    path.join(ROOT, "lit_review", meta.filename),
    "utf8",
  );
  const { content } = matter(raw);
  return { ...meta, content };
}

export function getResearchAgenda(): { content: string; updated: string } {
  const p = path.join(ROOT, "research_agenda.md");
  if (!fs.existsSync(p)) return { content: "", updated: "" };
  const raw = fs.readFileSync(p, "utf8");
  const { content, data } = matter(raw);
  return { content, updated: data.date ?? "" };
}

export function getWorklogs(): Array<{
  filename: string;
  week: number;
  dates: string;
  content: string;
}> {
  const dir = path.join(ROOT, "worklog");
  if (!fs.existsSync(dir)) return [];

  const files = fs
    .readdirSync(dir)
    .filter((f) => f.endsWith(".md"))
    .sort();

  return files.map((filename) => {
    const raw = fs.readFileSync(path.join(dir, filename), "utf8");
    const { data, content } = matter(raw);
    return {
      filename,
      week: data.week ?? 0,
      dates: data.dates ?? "",
      content,
    };
  });
}
