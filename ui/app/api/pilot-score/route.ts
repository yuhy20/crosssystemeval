import { NextResponse } from "next/server";
import { writePilotScores, type PilotScoreEntry } from "@/lib/pilot-score";

// Force this route to run on the Node runtime (fs access) and never be cached.
export const runtime = "nodejs";
export const dynamic = "force-dynamic";

interface PostBody {
  label?: string;
  scores?: Array<{ item_id?: number; score?: number | null; comment?: string }>;
}

export async function POST(req: Request) {
  // Local-only write. The deployed Vercel site stays read-only.
  if (process.env.NODE_ENV !== "development") {
    return NextResponse.json(
      { ok: false, error: "writes disabled outside development" },
      { status: 403 },
    );
  }

  let body: PostBody;
  try {
    body = (await req.json()) as PostBody;
  } catch {
    return NextResponse.json(
      { ok: false, error: "invalid JSON body" },
      { status: 400 },
    );
  }

  const label = typeof body.label === "string" ? body.label : "";
  if (!/^response_\d+$/.test(label)) {
    return NextResponse.json(
      { ok: false, error: "invalid or missing label" },
      { status: 400 },
    );
  }

  if (!Array.isArray(body.scores)) {
    return NextResponse.json(
      { ok: false, error: "scores must be an array" },
      { status: 400 },
    );
  }

  const cleaned: PilotScoreEntry[] = [];
  for (const s of body.scores) {
    const id = typeof s.item_id === "number" ? s.item_id : NaN;
    if (!Number.isInteger(id) || id < 1 || id > 10) {
      return NextResponse.json(
        { ok: false, error: `invalid item_id: ${s.item_id}` },
        { status: 400 },
      );
    }
    let score: number | null;
    if (s.score === null || s.score === undefined) {
      score = null;
    } else if (
      typeof s.score === "number" &&
      Number.isInteger(s.score) &&
      s.score >= 0 &&
      s.score <= 3
    ) {
      score = s.score;
    } else {
      return NextResponse.json(
        { ok: false, error: `invalid score for item ${id}: ${s.score}` },
        { status: 400 },
      );
    }
    const comment = typeof s.comment === "string" ? s.comment : "";
    cleaned.push({ item_id: id, score, comment });
  }

  const result = writePilotScores(label, cleaned);
  if (!result.ok) {
    return NextResponse.json(result, { status: 500 });
  }
  return NextResponse.json({ ok: true });
}
