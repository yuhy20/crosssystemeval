import fs from "node:fs";
import path from "node:path";

const ROOT = path.resolve(process.cwd(), "..");

export interface RubricAnchor {
  level: 0 | 1 | 2 | 3;
  text: string;
}

export interface RubricItem {
  id: number; // 1..10
  title: string; // e.g. "Identifies §9.60(c) as the controlling statutory test"
  source: string; // rule source line
  anchors: RubricAnchor[]; // 0..3
}

export interface PilotScoreEntry {
  item_id: number; // 1..10
  score: number | null; // 0..3 or null if blank
  comment: string; // empty string if blank
}

export interface PilotScoreState {
  label: string;
  scores: PilotScoreEntry[]; // length 10, items 1..10
  responseMarkdown: string; // the response body, for read-only render above the form
  preambleMarkdown: string; // header before the response, for context
}

// ---------------------------------------------------------------------------
// Rubric parser — extracts anchor text per item from rubrics/judge_v2_source_first.md
// ---------------------------------------------------------------------------

export function getRubricItems(): RubricItem[] {
  const p = path.join(ROOT, "rubrics", "judge_v2_source_first.md");
  if (!fs.existsSync(p)) return [];
  const raw = fs.readFileSync(p, "utf8");

  const items: RubricItem[] = [];
  // Match item blocks: "### N. <title>" followed by content until next "### " or EOF
  // Note: the rubric uses "### 1. Identifies..." (no "Item " prefix), whereas
  // the per-response sheets use "### Item 1. Identifies...". We parse the
  // rubric form here.
  const itemHeaderRe = /^###\s+(\d+)\.\s+(.+)$/gm;
  const headers: { id: number; title: string; index: number }[] = [];
  let m: RegExpExecArray | null;
  while ((m = itemHeaderRe.exec(raw)) !== null) {
    const id = parseInt(m[1], 10);
    if (id >= 1 && id <= 10) {
      headers.push({ id, title: m[2].trim(), index: m.index });
    }
  }

  for (let i = 0; i < headers.length; i++) {
    const h = headers[i];
    const end = i + 1 < headers.length ? headers[i + 1].index : raw.length;
    const block = raw.slice(h.index, end);

    // Source line: "**Source:** <text>"
    const sourceMatch = block.match(/\*\*Source:\*\*\s*(.+)/);
    const source = sourceMatch ? sourceMatch[1].trim() : "";

    // Anchors: "- **0** — text" through "- **3** — text" (em-dash or hyphen).
    // We parse line-by-line because anchor text occasionally wraps and we want
    // the whole logical bullet, but in practice the rubric keeps each anchor
    // on a single line. Tolerate either form.
    const anchors: RubricAnchor[] = [];
    const anchorLineRe = /^-\s+\*\*([0-3])\*\*\s+[—-]\s+(.+)$/;
    for (const line of block.split("\n")) {
      const am = line.match(anchorLineRe);
      if (am) {
        const level = parseInt(am[1], 10) as 0 | 1 | 2 | 3;
        anchors.push({ level, text: am[2].trim() });
      }
    }
    anchors.sort((a, b) => a.level - b.level);

    items.push({ id: h.id, title: h.title, source, anchors });
  }

  items.sort((a, b) => a.id - b.id);
  return items;
}

// ---------------------------------------------------------------------------
// Sheet parser — extracts current score / comment per item from a sheet file
// ---------------------------------------------------------------------------

function sheetPath(label: string): string {
  return path.join(
    ROOT,
    "data",
    "pilot",
    "judge_v2",
    "scoring_session_1",
    `${label}.md`,
  );
}

const SCORE_LINE_RE = /\*\*Score \(0 \/ 1 \/ 2 \/ 3\):\*\*\s*(.+?)\s*$/m;
const COMMENT_LINE_RE = /\*\*Comments:\*\*\s*(.+?)\s*$/m;

function parseScoreValue(raw: string): number | null {
  const trimmed = raw.trim();
  if (trimmed === "" || /^_+$/.test(trimmed)) return null;
  const n = parseInt(trimmed, 10);
  if (Number.isFinite(n) && n >= 0 && n <= 3 && String(n) === trimmed) return n;
  // Tolerate "2/3" or trailing punctuation by extracting first digit 0-3
  const m = trimmed.match(/^([0-3])\b/);
  if (m) return parseInt(m[1], 10);
  return null;
}

function parseCommentValue(raw: string): string {
  const trimmed = raw.trim();
  if (trimmed === "" || /^_+$/.test(trimmed)) return "";
  return trimmed;
}

export function readPilotScoreState(label: string): PilotScoreState | null {
  const p = sheetPath(label);
  if (!fs.existsSync(p)) return null;
  const raw = fs.readFileSync(p, "utf8");

  // Split into preamble, response body, and items section.
  // The response is between "## Response" and the "## Items" header.
  const responseStart = raw.indexOf("\n## Response");
  const itemsStart = raw.indexOf("\n## Items");

  let preambleMarkdown = "";
  let responseMarkdown = "";
  let itemsSection = raw;
  if (responseStart >= 0 && itemsStart > responseStart) {
    preambleMarkdown = raw.slice(0, responseStart).trim();
    // Skip the "## Response" heading itself when rendering body.
    const afterResponseHeader = raw.indexOf("\n", responseStart + 1) + 1;
    responseMarkdown = raw.slice(afterResponseHeader, itemsStart).trim();
    // Strip a trailing horizontal rule that separates body from items.
    responseMarkdown = responseMarkdown.replace(/\n-{3,}\s*$/, "").trim();
    itemsSection = raw.slice(itemsStart);
  }

  // Parse each item block in the items section.
  const itemHeaderRe = /^###\s+Item\s+(\d+)\./gm;
  const headers: { id: number; index: number }[] = [];
  let m: RegExpExecArray | null;
  while ((m = itemHeaderRe.exec(itemsSection)) !== null) {
    const id = parseInt(m[1], 10);
    if (id >= 1 && id <= 10) headers.push({ id, index: m.index });
  }

  const scores: PilotScoreEntry[] = [];
  for (let i = 0; i < headers.length; i++) {
    const h = headers[i];
    const end = i + 1 < headers.length ? headers[i + 1].index : itemsSection.length;
    const block = itemsSection.slice(h.index, end);

    const sm = block.match(SCORE_LINE_RE);
    const cm = block.match(COMMENT_LINE_RE);
    scores.push({
      item_id: h.id,
      score: sm ? parseScoreValue(sm[1]) : null,
      comment: cm ? parseCommentValue(cm[1]) : "",
    });
  }

  // Ensure all 10 entries present, in order.
  const byId = new Map(scores.map((s) => [s.item_id, s]));
  const filled: PilotScoreEntry[] = [];
  for (let id = 1; id <= 10; id++) {
    filled.push(byId.get(id) ?? { item_id: id, score: null, comment: "" });
  }

  return {
    label,
    scores: filled,
    responseMarkdown,
    preambleMarkdown,
  };
}

// ---------------------------------------------------------------------------
// Serializer — write scores back into the sheet, preserving everything else
// ---------------------------------------------------------------------------

function formatScore(score: number | null): string {
  return score === null ? "____" : String(score);
}

function formatComment(comment: string): string {
  // Trim and collapse any newlines to keep the line single-line in markdown.
  const cleaned = comment.replace(/\r?\n+/g, " ").trim();
  return cleaned === "" ? "____" : cleaned;
}

export function writePilotScores(
  label: string,
  scores: PilotScoreEntry[],
): { ok: true } | { ok: false; error: string } {
  const p = sheetPath(label);
  if (!fs.existsSync(p)) {
    return { ok: false, error: `sheet not found: ${label}` };
  }
  const raw = fs.readFileSync(p, "utf8");

  // Find each item block and replace its score + comment line in place.
  // We operate on the slice from "## Items" onward to avoid touching the response body.
  const itemsStart = raw.indexOf("\n## Items");
  if (itemsStart < 0) {
    return { ok: false, error: "items section not found in sheet" };
  }
  const before = raw.slice(0, itemsStart);
  let itemsSection = raw.slice(itemsStart);

  const itemHeaderRe = /^###\s+Item\s+(\d+)\./gm;
  const headers: { id: number; index: number }[] = [];
  let m: RegExpExecArray | null;
  while ((m = itemHeaderRe.exec(itemsSection)) !== null) {
    const id = parseInt(m[1], 10);
    if (id >= 1 && id <= 10) headers.push({ id, index: m.index });
  }

  const scoreById = new Map(scores.map((s) => [s.item_id, s]));

  // Walk blocks in reverse so indices stay valid when we rewrite slices.
  for (let i = headers.length - 1; i >= 0; i--) {
    const h = headers[i];
    const end = i + 1 < headers.length ? headers[i + 1].index : itemsSection.length;
    const entry = scoreById.get(h.id);
    if (!entry) continue;

    const block = itemsSection.slice(h.index, end);
    const newScoreLine = `**Score (0 / 1 / 2 / 3):** ${formatScore(entry.score)}`;
    const newCommentLine = `**Comments:** ${formatComment(entry.comment)}`;
    const updated = block
      .replace(/\*\*Score \(0 \/ 1 \/ 2 \/ 3\):\*\*[^\n]*/, newScoreLine)
      .replace(/\*\*Comments:\*\*[^\n]*/, newCommentLine);

    itemsSection = itemsSection.slice(0, h.index) + updated + itemsSection.slice(end);
  }

  const next = before + itemsSection;
  fs.writeFileSync(p, next, "utf8");
  return { ok: true };
}

// ---------------------------------------------------------------------------
// Convenience: combined view-model for the page
// ---------------------------------------------------------------------------

export interface PilotScoreView {
  label: string;
  rubric: RubricItem[];
  scores: PilotScoreEntry[];
  responseMarkdown: string;
}

export function getPilotScoreView(label: string): PilotScoreView | null {
  const state = readPilotScoreState(label);
  if (!state) return null;
  return {
    label,
    rubric: getRubricItems(),
    scores: state.scores,
    responseMarkdown: state.responseMarkdown,
  };
}
