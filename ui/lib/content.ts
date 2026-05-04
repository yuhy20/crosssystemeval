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

// ---------------------------------------------------------------------------
// Pilot — Judge Rubric v1
// ---------------------------------------------------------------------------

export interface PilotResponseEntry {
  label: string;          // anonymized session-1 label, e.g. "response_03"
  prompt_id: string;
  framing: string;
  question: string;
  model: string;
  charCount: number;
}

export interface PilotData {
  responses: PilotResponseEntry[];
  rubricMarkdown: string;
  promptsMarkdown: string;
  scoringSheetTemplate: string;
  generatedAt: string | null;
  modelsUsed: string[];
  promptIds: string[];
}

interface RawCell {
  model: string;
  prompt_id: string;
  framing: string;
  question: string;
  user_message: string;
  response: string | null;
  error: string | null;
  temperature: number;
  max_tokens: number;
  started_at: string;
  finished_at: string;
}

function readRawCells(): RawCell[] {
  const p = path.join(ROOT, "data", "pilot", "judge_v1", "responses.jsonl");
  if (!fs.existsSync(p)) return [];
  return fs
    .readFileSync(p, "utf8")
    .split("\n")
    .filter((l) => l.trim().length > 0)
    .map((l) => JSON.parse(l) as RawCell);
}

function readSession1Key(): Map<string, { model: string; prompt_id: string }> {
  // Maps anonymized session-1 label → (model, prompt_id) using SCORING_KEY.md.
  const p = path.join(
    ROOT,
    "data",
    "pilot",
    "judge_v1",
    "scoring_session_1",
    "SCORING_KEY.md",
  );
  const map = new Map<string, { model: string; prompt_id: string }>();
  if (!fs.existsSync(p)) return map;
  const raw = fs.readFileSync(p, "utf8");
  for (const line of raw.split("\n")) {
    const m = line.match(/^\| (response_\d+) \| ([^|]+) \| ([^|]+) \|/);
    if (m) {
      map.set(m[1], { model: m[2].trim(), prompt_id: m[3].trim() });
    }
  }
  return map;
}

export function getPilotData(): PilotData {
  const cells = readRawCells();
  const sess1 = readSession1Key();

  const cellByKey = new Map<string, RawCell>();
  for (const c of cells) {
    cellByKey.set(`${c.model}::${c.prompt_id}`, c);
  }

  const responses: PilotResponseEntry[] = [];
  // Walk session-1 labels in their shuffled order so the UI shows the same
  // anonymized order the scorer sees in scoring_session_1/.
  const labels = Array.from(sess1.keys()).sort();
  for (const label of labels) {
    const ref = sess1.get(label);
    if (!ref) continue;
    const cell = cellByKey.get(`${ref.model}::${ref.prompt_id}`);
    if (!cell) continue;
    responses.push({
      label,
      prompt_id: cell.prompt_id,
      framing: cell.framing,
      question: cell.question,
      model: cell.model,
      charCount: (cell.response ?? "").length,
    });
  }

  const safeRead = (rel: string): string => {
    const p = path.join(ROOT, rel);
    return fs.existsSync(p) ? fs.readFileSync(p, "utf8") : "";
  };

  return {
    responses,
    rubricMarkdown: safeRead("rubrics/judge_v1.md"),
    promptsMarkdown: safeRead("rubrics/pilot_prompts.md"),
    scoringSheetTemplate: safeRead("rubrics/scoring_sheet_template.md"),
    generatedAt: cells[0]?.finished_at ?? null,
    modelsUsed: Array.from(new Set(cells.map((c) => c.model))),
    promptIds: Array.from(new Set(cells.map((c) => c.prompt_id))),
  };
}

export interface PilotSheet {
  label: string;
  prompt_id: string;
  framing: string;
  question: string;
  // Note: model is intentionally NOT exposed here — keeps the UI blind.
  // The scorer can look it up post-scoring via SCORING_KEY.md on disk.
  sheetMarkdown: string;
}

export function getPilotSheet(label: string): PilotSheet | null {
  const data = getPilotData();
  const entry = data.responses.find((r) => r.label === label);
  if (!entry) return null;
  const p = path.join(
    ROOT,
    "data",
    "pilot",
    "judge_v1",
    "scoring_session_1",
    `${label}.md`,
  );
  if (!fs.existsSync(p)) return null;
  return {
    label: entry.label,
    prompt_id: entry.prompt_id,
    framing: entry.framing,
    question: entry.question,
    sheetMarkdown: fs.readFileSync(p, "utf8"),
  };
}
