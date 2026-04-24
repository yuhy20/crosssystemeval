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
        eyebrow="Validation Stack · Layer 1 of 5"
        title="Jury Substitution Calibration"
        description="Validates that our substitute jury (Claude Sonnet 4.6 + Llama 3.1 8B Instant, replacing TRIDENT's decommissioned Claude 3.5 Sonnet + Gemma 2-9B) produces scalar harmfulness scores within ±0.3 of TRIDENT Figure 4 published means. This is calibration — not replication — and it validates only the inference pipeline layer. Layers 2 through 5 of the validation stack remain to be executed in Weeks 2–4."
      />

      <Section>
        <SoftCard className="animate-fade-up-delay-1">
          <div className="flex items-start gap-4">
            <div className="mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-status-success/15 text-status-success ring-1 ring-inset ring-status-success/25">
              <CheckCircle2 className="h-5 w-5" strokeWidth={2} />
            </div>
            <div className="min-w-0">
              <div className="font-display text-[17px] font-semibold tracking-tight text-ink">
                Layer 1 validated — 6 of 6 calibration cells PASS
              </div>
              <p className="mt-2 text-[14.5px] leading-relaxed text-ink-secondary">
                Observed mean harmfulness for GPT-4o and GPT-4o-mini across all three TRIDENT domains (law, med, finance) falls within ±0.3 of TRIDENT Figure 4's published means using our substitute jury. This validates the inference pipeline layer of the methodology. It does <strong className="text-ink">not</strong> validate rubric-item judge reliability, rubric construct validity, statistical power, or ICR construct validity — those layers are separately scheduled.
              </p>
            </div>
          </div>
        </SoftCard>
      </Section>

      <Section title="Results (n=30 target, seed=42, ±0.3 tolerance)">
        <div className="animate-fade-up-delay-2 space-y-5">
          <ResultsTable />
          <p className="text-[12px] leading-relaxed text-ink-muted">
            <strong className="text-ink-secondary">κ<sub>judge</sub> / r<sub>judge</sub></strong>: inter-judge agreement between Judge A and Judge B scores on the same responses. Validates that the two-model jury produces consistent ratings (upstream pipeline QA). Distinct from <code className="rounded bg-surface-muted px-1 py-0.5 font-mono text-[11.5px]">κ_human</code> (Phase 1 rubric validation) and <code className="rounded bg-surface-muted px-1 py-0.5 font-mono text-[11.5px]">r_H2</code> (discriminant test between ICR and sycophancy). Some runs have n&lt;30 due to Groq free-tier rate limiting — partial-failure resilience kept the remaining records clean rather than aborting the run.
          </p>
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
            Chart regenerated from <code className="rounded bg-surface-muted px-1 py-0.5 font-mono text-[11.5px] text-ink-secondary">code/trident_repro/outputs/clean_*.jsonl</code> via{" "}
            <code className="rounded bg-surface-muted px-1 py-0.5 font-mono text-[11.5px] text-ink-secondary">python scripts/render_results.py</code>.
          </p>
        </div>
      </Section>

      <Section title="Jury substitution trail">
        <SoftCard className="animate-fade-up-delay-3">
          <p className="mb-4 text-[14.5px] leading-relaxed text-ink-secondary">
            TRIDENT used Claude 3.5 Sonnet + Gemma 2-9B. Neither is accessible on our stack. We substitute in-spirit:
          </p>
          <div className="overflow-hidden rounded-lg ring-1 ring-inset ring-ink-hairline/60">
            <table className="w-full text-left text-[13px]">
              <thead className="bg-surface-muted text-[11px] font-semibold uppercase tracking-[0.08em] text-ink-muted">
                <tr>
                  <th className="px-4 py-2">Role</th>
                  <th className="px-4 py-2">TRIDENT</th>
                  <th className="px-4 py-2">Ours</th>
                  <th className="px-4 py-2">Rationale</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-b border-ink-hairline/50">
                  <td className="px-4 py-3 text-ink font-mono text-[12px]">Judge A</td>
                  <td className="px-4 py-3 text-ink-muted font-mono text-[12px]">claude-3-5-sonnet</td>
                  <td className="px-4 py-3 text-ink font-mono text-[12px]">claude-sonnet-4-6</td>
                  <td className="px-4 py-3 text-ink-secondary">3.5 deprecated on new Anthropic accounts; 4.6 is same-vendor flagship</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 text-ink font-mono text-[12px]">Judge B</td>
                  <td className="px-4 py-3 text-ink-muted font-mono text-[12px]">gemma-2-9b</td>
                  <td className="px-4 py-3 text-ink font-mono text-[12px]">llama-3.1-8b-instant</td>
                  <td className="px-4 py-3 text-ink-secondary">Gemma 2-9B decommissioned by Groq. Llama 3.1 8B is closest open-weight substitute (~8B params, non-Anthropic/non-OpenAI)</td>
                </tr>
              </tbody>
            </table>
          </div>
          <p className="mt-4 text-[13px] leading-relaxed text-ink-muted">
            <strong className="text-ink-secondary">Calibration, not replication.</strong> We validate that our pipeline produces
            TRIDENT-consistent harmfulness scores on reference models (GPT-4o, GPT-4o-mini) within ±0.3 tolerance. We do
            not reproduce TRIDENT's full 19-model study — most of their domain-specialized targets (DISC-LawLLM, Meditron,
            Saul-7B, FinGPT, etc.) are not hosted by any accessible inference provider and would require self-hosted GPU
            infrastructure. A strict replication is out of scope; our research question is about novel cross-system
            scenarios, not reproduction of TRIDENT findings.
          </p>
        </SoftCard>
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
