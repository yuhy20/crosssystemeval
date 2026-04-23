import Image from "next/image";
import { CheckCircle2, Circle } from "lucide-react";
import { Page, PageHeader, Section } from "@/components/Container";
import { SoftCard } from "@/components/Card";
import ResultsTable from "@/components/ResultsTable";

const modules: Array<{ name: string; note: string; status: "done" | "pending" }> = [
  { name: "pyproject.toml", note: "Pinned deps, hatchling, strict mypy, ruff, pytest w/ 70% cov gate", status: "done" },
  { name: "README.md", note: "uv-first setup, CLI usage", status: "done" },
  { name: ".env.example", note: "API key template", status: "done" },
  { name: ".gitignore", note: "Exclude .env, outputs, __pycache__", status: "done" },
  { name: "src/trident_repro/__init__.py", note: "Public re-exports + version", status: "done" },
  { name: "src/trident_repro/config.py", note: "Pydantic Settings + RunConfig dataclass", status: "done" },
  { name: "src/trident_repro/loader.py", note: "Deterministic JSONL sampling", status: "done" },
  { name: "src/trident_repro/models.py", note: "Anthropic + OpenAI clients, tenacity retries", status: "done" },
  { name: "src/trident_repro/judge.py", note: "Harmfulness jury, 3-tier JSON parser", status: "done" },
  { name: "src/trident_repro/pipeline.py", note: "Crash-safe JSONL streaming, resume, partial-failure tolerance", status: "done" },
  { name: "src/trident_repro/metrics.py", note: "Cohen's κ, Pearson r, published-mean comparison", status: "done" },
  { name: "src/trident_repro/cli.py", note: "click-based CLI", status: "done" },
  { name: "scripts/render_results.py", note: "Emits ui/public/trident/ PNG + JSON from outputs/", status: "done" },
  { name: "tests/conftest.py", note: "FakeChatClient + tiny_dataset_dir fixtures", status: "done" },
  { name: "tests/test_loader.py", note: "Schema + determinism + domain filter (14 tests)", status: "done" },
  { name: "tests/test_judge.py", note: "Mock jury, 3-tier parser, clamping (11 tests)", status: "done" },
  { name: "tests/test_pipeline.py", note: "End-to-end, resume, partial-failure, durability (5 tests)", status: "done" },
  { name: "notebooks/calibration_check.ipynb", note: "Load → aggregate → bar chart → κ → PASS/FAIL", status: "done" },
];

const doneCount = modules.filter((m) => m.status === "done").length;

export default function TridentPage() {
  return (
    <Page>
      <PageHeader
        eyebrow="Calibration harness"
        title="TRIDENT Replication"
        description="Before scoring novel CrossSystemEval scenarios, validate the LLM-as-judge pipeline by replicating TRIDENT's harmfulness score distribution on a 30-prompt subset. Production-quality Python package; mock-based tests; uv-first setup."
      />

      <Section>
        <SoftCard className="animate-fade-up-delay-1">
          <div className="flex items-start gap-4">
            <div className="mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-status-success/15 text-status-success ring-1 ring-inset ring-status-success/25">
              <CheckCircle2 className="h-5 w-5" strokeWidth={2} />
            </div>
            <div className="min-w-0">
              <div className="font-display text-[17px] font-semibold tracking-tight text-ink">
                Calibration PASSED on both TRIDENT-referenced models
              </div>
              <p className="mt-2 text-[14.5px] leading-relaxed text-ink-secondary">
                Harness mean harmfulness scores agreed with TRIDENT Figure 4 to within ±0.1 on GPT-4o and GPT-4o-mini — well inside the ±0.3 calibration tolerance. Three Claude 4.x models baselined without a TRIDENT reference (observed-only).
              </p>
            </div>
          </div>
        </SoftCard>
      </Section>

      <Section title="Results (law domain, n=30, seed=42)">
        <div className="animate-fade-up-delay-2 space-y-5">
          <ResultsTable />
          <SoftCard className="p-3">
            <Image
              src="/trident/calibration_chart.png"
              alt="Calibration chart: observed vs. TRIDENT published harmfulness means"
              width={2600}
              height={1040}
              className="w-full rounded-lg"
              priority
            />
          </SoftCard>
          <p className="text-[12.5px] leading-relaxed text-ink-muted">
            Chart regenerated from <code className="rounded bg-surface-muted px-1 py-0.5 font-mono text-[11.5px] text-ink-secondary">code/trident_repro/outputs/*.jsonl</code> via{" "}
            <code className="rounded bg-surface-muted px-1 py-0.5 font-mono text-[11.5px] text-ink-secondary">python scripts/render_results.py</code>. Re-run after any new calibration to refresh this page.
          </p>
        </div>
      </Section>

      <Section title="Run it">
        <SoftCard className="animate-fade-up-delay-3">
          <pre className="overflow-x-auto rounded-lg bg-surface p-5 font-mono text-[12.5px] leading-relaxed text-ink ring-1 ring-inset ring-white/5">
            <span className="text-ink-muted"># setup</span>{"\n"}
            cd /Users/yunheehyun/crosssystemeval/code/trident_repro{"\n"}
            uv venv && uv pip install -e ".[dev]"{"\n"}
            cp .env.example .env  <span className="text-ink-muted"># add ANTHROPIC_API_KEY + OPENAI_API_KEY</span>{"\n\n"}
            <span className="text-ink-muted"># verify tests (mock-based, no API calls)</span>{"\n"}
            pytest{"\n\n"}
            <span className="text-ink-muted"># calibrate</span>{"\n"}
            trident-repro run --n 30 --domain law --seed 42 --target-model gpt-4o \{"\n"}
            {"  "}--judge-a gpt-4o --judge-b gpt-4o-mini \{"\n"}
            {"  "}--output outputs/gpt-4o_law.jsonl{"\n\n"}
            <span className="text-ink-muted"># refresh this page</span>{"\n"}
            python scripts/render_results.py
          </pre>
        </SoftCard>
      </Section>

      <Section title="Module inventory">
        <div className="animate-fade-up-delay-3 overflow-hidden rounded-xl bg-surface-elevated shadow-card">
          <table className="w-full text-left">
            <thead className="bg-surface-muted text-[12px] font-semibold uppercase tracking-[0.08em] text-ink-muted">
              <tr>
                <th className="w-12 px-6 py-3"></th>
                <th className="px-6 py-3">File</th>
                <th className="px-6 py-3">Responsibility</th>
              </tr>
            </thead>
            <tbody className="text-[14px]">
              {modules.map((m, i) => (
                <tr
                  key={m.name}
                  className={
                    i !== modules.length - 1
                      ? "border-b border-ink-hairline/70"
                      : ""
                  }
                >
                  <td className="px-6 py-4">
                    <CheckCircle2
                      className="h-4 w-4 text-status-success"
                      strokeWidth={2}
                    />
                  </td>
                  <td className="px-6 py-4 font-mono text-[13px] text-ink">
                    {m.name}
                  </td>
                  <td className="px-6 py-4 text-ink-secondary">{m.note}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="border-t border-ink-hairline/70 bg-surface-muted/50 px-6 py-3 text-[12.5px] text-ink-muted">
            {doneCount} / {modules.length} complete
          </div>
        </div>
      </Section>

      <Section title="Success criterion">
        <SoftCard className="animate-fade-up-delay-3">
          <div className="flex items-start gap-4">
            <div className="mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-status-info/15 text-status-info ring-1 ring-inset ring-status-info/25">
              <Circle className="h-5 w-5" strokeWidth={2} />
            </div>
            <div>
              <div className="font-display text-[17px] font-semibold tracking-tight text-ink">
                Mean harmfulness within ±0.3 of TRIDENT's published score
              </div>
              <p className="mt-2 text-[14.5px] leading-relaxed text-ink-secondary">
                Observed: GPT-4o 1.367 (Δ −0.033), GPT-4o-mini 1.467 (Δ +0.067). Both PASS. For Claude 4.x models, TRIDENT has no Figure 4 reference mean — we report observed baselines only.
              </p>
            </div>
          </div>
        </SoftCard>
      </Section>
    </Page>
  );
}
