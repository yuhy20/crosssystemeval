import clsx from "clsx";
import fs from "node:fs";
import path from "node:path";

interface Row {
  run: string;
  target_model: string;
  n: number;
  observed_mean: number;
  published_mean: number | null;
  delta: number | null;
  within_tolerance: boolean | null;
  judge_a: string;
  judge_b: string;
  cohen_kappa: number | null;
  pearson_r: number | null;
  exact_agreement_pct: number | null;
  verdict: "PASS" | "FAIL" | "N/A";
}

interface Results {
  tolerance: number;
  rows: Row[];
}

function loadResults(): Results | null {
  const p = path.join(process.cwd(), "public", "trident", "results.json");
  if (!fs.existsSync(p)) return null;
  return JSON.parse(fs.readFileSync(p, "utf8"));
}

function fmt(n: number | null, digits = 3): string {
  if (n === null || n === undefined) return "—";
  return n.toFixed(digits);
}

function signedFmt(n: number | null, digits = 3): string {
  if (n === null || n === undefined) return "—";
  const v = n.toFixed(digits);
  return n >= 0 ? `+${v}` : v;
}

const verdictStyle: Record<Row["verdict"], string> = {
  PASS: "bg-status-success/15 text-status-success ring-1 ring-inset ring-status-success/30",
  FAIL: "bg-status-danger/15 text-status-danger ring-1 ring-inset ring-status-danger/30",
  "N/A": "bg-ink-faint/30 text-ink-muted ring-1 ring-inset ring-ink-faint/40",
};

export default function ResultsTable() {
  const results = loadResults();

  if (!results) {
    return (
      <div className="rounded-xl bg-surface-elevated p-6 shadow-card text-[14px] text-ink-muted">
        No results yet. Run{" "}
        <code className="rounded bg-surface-muted px-1.5 py-0.5 font-mono text-[12.5px] text-ink">
          python scripts/render_results.py
        </code>{" "}
        in the <code className="rounded bg-surface-muted px-1.5 py-0.5 font-mono text-[12.5px] text-ink">trident_repro</code> directory to generate them.
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-xl bg-surface-elevated shadow-card">
      <table className="w-full text-left">
        <thead className="bg-surface-muted text-[11px] font-semibold uppercase tracking-[0.08em] text-ink-muted">
          <tr>
            <th className="px-4 py-3">Target</th>
            <th className="px-4 py-3 text-right">n</th>
            <th className="px-4 py-3 text-right">Observed</th>
            <th className="px-4 py-3 text-right">Published</th>
            <th className="px-4 py-3 text-right">Δ</th>
            <th className="px-4 py-3 text-right">κ</th>
            <th className="px-4 py-3 text-right">Pearson r</th>
            <th className="px-4 py-3 text-right">Exact %</th>
            <th className="px-4 py-3">Jury</th>
            <th className="px-4 py-3 text-center">Verdict</th>
          </tr>
        </thead>
        <tbody className="text-[13px] font-mono">
          {results.rows.map((r, i) => (
            <tr
              key={r.run}
              className={
                i !== results.rows.length - 1
                  ? "border-b border-ink-hairline/60"
                  : ""
              }
            >
              <td className="px-4 py-3 text-ink">{r.target_model}</td>
              <td className="px-4 py-3 text-right text-ink-secondary">{r.n}</td>
              <td className="px-4 py-3 text-right text-ink">{fmt(r.observed_mean)}</td>
              <td className="px-4 py-3 text-right text-ink-secondary">{fmt(r.published_mean)}</td>
              <td className="px-4 py-3 text-right text-ink-secondary">
                {signedFmt(r.delta)}
              </td>
              <td className="px-4 py-3 text-right text-ink-secondary">{fmt(r.cohen_kappa)}</td>
              <td className="px-4 py-3 text-right text-ink-secondary">{fmt(r.pearson_r)}</td>
              <td className="px-4 py-3 text-right text-ink-secondary">{fmt(r.exact_agreement_pct, 1)}</td>
              <td className="px-4 py-3 text-[11.5px] text-ink-muted">
                {r.judge_a.replace("claude-", "C-").replace("gpt-", "G-")}
                <br />
                {r.judge_b.replace("claude-", "C-").replace("gpt-", "G-")}
              </td>
              <td className="px-4 py-3 text-center">
                <span
                  className={clsx(
                    "rounded-full px-2 py-0.5 text-[11px] font-semibold uppercase tracking-wider",
                    verdictStyle[r.verdict],
                  )}
                >
                  {r.verdict}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
