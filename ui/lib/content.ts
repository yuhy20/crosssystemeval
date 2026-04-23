import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";

const ROOT = path.resolve(process.cwd(), "..");

// YAML parses bare dates as JS Date objects. We never want to pass those
// to React directly — stringify to YYYY-MM-DD. Everything else falls back
// to `String(value)` so weird types don't crash the render.
function asString(value: unknown, fallback = ""): string {
  if (value === undefined || value === null) return fallback;
  if (value instanceof Date) return value.toISOString().slice(0, 10);
  if (typeof value === "string") return value;
  if (typeof value === "number" || typeof value === "boolean") return String(value);
  return fallback;
}

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
      slug: asString(data.slug),
      title: asString(data.title),
      subtitle: asString(data.subtitle),
      papers: typeof data.papers === "number" ? data.papers : 0,
      status: asString(data.status, "draft"),
      date: asString(data.date),
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
  return { content, updated: asString(data.date) };
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
      week: typeof data.week === "number" ? data.week : 0,
      dates: asString(data.dates),
      content,
    };
  });
}
