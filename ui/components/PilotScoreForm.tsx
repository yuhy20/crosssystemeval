"use client";

import { useMemo, useState } from "react";
import type { PilotScoreEntry, RubricItem } from "@/lib/pilot-score";

interface Props {
  label: string;
  rubric: RubricItem[];
  initialScores: PilotScoreEntry[];
}

type SaveStatus =
  | { kind: "idle" }
  | { kind: "saving" }
  | { kind: "ok"; at: number }
  | { kind: "error"; message: string };

const SCORE_OPTIONS: Array<0 | 1 | 2 | 3> = [0, 1, 2, 3];

export default function PilotScoreForm({
  label,
  rubric,
  initialScores,
}: Props) {
  const [entries, setEntries] = useState<PilotScoreEntry[]>(initialScores);
  const [status, setStatus] = useState<SaveStatus>({ kind: "idle" });

  const rubricById = useMemo(() => {
    const m = new Map<number, RubricItem>();
    for (const r of rubric) m.set(r.id, r);
    return m;
  }, [rubric]);

  function updateScore(id: number, score: number | null) {
    setEntries((prev) =>
      prev.map((e) => (e.item_id === id ? { ...e, score } : e)),
    );
  }

  function updateComment(id: number, comment: string) {
    setEntries((prev) =>
      prev.map((e) => (e.item_id === id ? { ...e, comment } : e)),
    );
  }

  async function handleSave() {
    setStatus({ kind: "saving" });
    try {
      const res = await fetch("/api/pilot-score", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ label, scores: entries }),
      });
      const data = (await res.json()) as { ok?: boolean; error?: string };
      if (!res.ok || !data.ok) {
        setStatus({
          kind: "error",
          message: data.error ?? `save failed (${res.status})`,
        });
        return;
      }
      setStatus({ kind: "ok", at: Date.now() });
    } catch (err) {
      setStatus({
        kind: "error",
        message: err instanceof Error ? err.message : "network error",
      });
    }
  }

  const roleSum = entries
    .filter((e) => e.item_id >= 1 && e.item_id <= 7 && e.score !== null)
    .reduce((a, e) => a + (e.score ?? 0), 0);
  const bleedSum = entries
    .filter((e) => e.item_id >= 8 && e.item_id <= 10 && e.score !== null)
    .reduce((a, e) => a + (e.score ?? 0), 0);
  const totalSum = roleSum + bleedSum;
  const allScored = entries.every((e) => e.score !== null);

  return (
    <div className="space-y-6">
      <div className="rounded-xl border border-ink-faint/40 bg-surface-elevated p-5 shadow-card">
        <div className="flex flex-wrap items-baseline justify-between gap-3 text-[13px] text-ink-secondary">
          <div className="font-semibold uppercase tracking-[0.08em] text-ink-muted">
            Running totals (live · not yet saved)
          </div>
          <div className="flex items-center gap-5">
            <span>
              Role 1–7:{" "}
              <span className="font-semibold text-ink">{roleSum}</span> / 21
            </span>
            <span>
              Bleed 8–10:{" "}
              <span className="font-semibold text-ink">{bleedSum}</span> / 9
            </span>
            <span>
              Total: <span className="font-semibold text-ink">{totalSum}</span>{" "}
              / 30
            </span>
            {!allScored && (
              <span className="text-ink-muted">
                ({entries.filter((e) => e.score !== null).length} / 10 scored)
              </span>
            )}
          </div>
        </div>
      </div>

      <ol className="space-y-5">
        {entries.map((entry) => {
          const item = rubricById.get(entry.item_id);
          return (
            <li
              key={entry.item_id}
              className="rounded-xl border border-ink-faint/40 bg-surface-elevated p-6 shadow-card"
            >
              <div className="mb-1 text-[11px] font-semibold uppercase tracking-[0.08em] text-ink-muted">
                Item {entry.item_id}
              </div>
              <h3 className="font-display text-[18px] font-semibold leading-snug tracking-tight text-ink">
                {item?.title ?? `(no rubric title for item ${entry.item_id})`}
              </h3>
              {item?.source && (
                <div className="mt-1 text-[12.5px] italic text-ink-muted">
                  Source: {item.source}
                </div>
              )}

              {item && item.anchors.length > 0 && (
                <ul className="mt-4 space-y-1.5 text-[13.5px] leading-relaxed text-ink-secondary">
                  {item.anchors.map((a) => (
                    <li key={a.level} className="flex gap-2">
                      <span className="shrink-0 font-semibold text-ink">
                        {a.level} —
                      </span>
                      <span>{a.text}</span>
                    </li>
                  ))}
                </ul>
              )}

              <div className="mt-5">
                <div className="mb-2 text-[12px] font-semibold uppercase tracking-[0.08em] text-ink-muted">
                  Score
                </div>
                <div
                  className="flex flex-wrap items-center gap-2"
                  role="radiogroup"
                  aria-label={`Score for item ${entry.item_id}`}
                >
                  {SCORE_OPTIONS.map((n) => {
                    const selected = entry.score === n;
                    return (
                      <button
                        key={n}
                        type="button"
                        role="radio"
                        aria-checked={selected}
                        onClick={() => updateScore(entry.item_id, n)}
                        className={
                          "h-10 w-10 rounded-md border text-[15px] font-semibold transition-colors " +
                          (selected
                            ? "border-accent bg-accent text-white"
                            : "border-ink-faint/60 bg-surface text-ink hover:border-accent/60")
                        }
                      >
                        {n}
                      </button>
                    );
                  })}
                  <button
                    type="button"
                    onClick={() => updateScore(entry.item_id, null)}
                    className={
                      "ml-1 rounded-md border px-3 py-2 text-[12.5px] font-medium transition-colors " +
                      (entry.score === null
                        ? "border-ink-faint bg-surface-muted text-ink"
                        : "border-ink-faint/60 bg-surface text-ink-muted hover:text-ink")
                    }
                  >
                    Clear
                  </button>
                </div>
              </div>

              <div className="mt-5">
                <label
                  className="mb-2 block text-[12px] font-semibold uppercase tracking-[0.08em] text-ink-muted"
                  htmlFor={`comment-${entry.item_id}`}
                >
                  Comments
                </label>
                <textarea
                  id={`comment-${entry.item_id}`}
                  value={entry.comment}
                  onChange={(e) => updateComment(entry.item_id, e.target.value)}
                  rows={2}
                  placeholder="Optional — note any evidence or ambiguity that drove the score."
                  className="w-full resize-y rounded-md border border-ink-faint/60 bg-surface px-3 py-2 text-[14px] leading-relaxed text-ink placeholder:text-ink-muted/70 focus:border-accent focus:outline-none focus:ring-1 focus:ring-accent/40"
                />
              </div>
            </li>
          );
        })}
      </ol>

      <div className="sticky bottom-4 z-10 flex flex-wrap items-center justify-between gap-3 rounded-xl border border-ink-faint/50 bg-surface-elevated/95 p-4 shadow-card backdrop-blur">
        <div className="text-[13px] text-ink-secondary">
          {status.kind === "ok" && (
            <span className="text-status-success">
              Saved to scoring_session_1/{label}.md
            </span>
          )}
          {status.kind === "error" && (
            <span className="text-status-danger">Error: {status.message}</span>
          )}
          {status.kind === "saving" && (
            <span className="text-ink-muted">Saving…</span>
          )}
          {status.kind === "idle" && (
            <span className="text-ink-muted">
              Writes to data/pilot/judge_v2/scoring_session_1/{label}.md
            </span>
          )}
        </div>
        <button
          type="button"
          onClick={handleSave}
          disabled={status.kind === "saving"}
          className="rounded-md bg-accent px-5 py-2 text-[14px] font-semibold text-white shadow-sm transition-opacity hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {status.kind === "saving" ? "Saving…" : "Save scores"}
        </button>
      </div>
    </div>
  );
}
