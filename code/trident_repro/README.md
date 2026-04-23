# trident-repro

A small, production-grade Python package that replicates a subset of
[**TRIDENT**](https://arxiv.org/abs/2507.21134) (2507.21134) for
**LLM-as-judge calibration** on professional-domain harmful prompts
(law, medicine, finance).

The package:

1. Loads TRIDENT `*_final.jsonl` prompts.
2. Sends each `harmful_prompt` to a **target model** (the model under test).
3. Has a **2-model jury** (Claude 3.5 Sonnet + GPT-4o-mini, substituting for
   Gemma 2-9B in the paper) score each response on a 1-5 harmfulness scale.
4. Writes crash-safe JSONL run records.
5. Aggregates results, computes inter-judge agreement (Cohen's kappa,
   Pearson r), and compares to hardcoded TRIDENT published means.

> **Scope:** This is a calibration harness, not a full TRIDENT reproduction.
> Target-model fine-tuning (the DPO side of the paper) is out of scope.

---

## Quickstart (uv, recommended)

```bash
cd /Users/yunheehyun/crosssystemeval/code/trident_repro

# 1. Create venv and install (editable, with dev extras)
uv venv
uv pip install -e ".[dev]"

# 2. Set credentials
cp .env.example .env
# then edit .env to add ANTHROPIC_API_KEY and OPENAI_API_KEY

# 3. Show CLI
trident-repro run --help

# 4. Run a small calibration (30 law prompts, seed 42)
trident-repro run \
    --n 30 \
    --domain law \
    --target-model claude-3-5-sonnet-20241022 \
    --seed 42
```

### Pip fallback

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

---

## CLI

```
trident-repro run --n <int> \
                  --domain {law,med,finance,all} \
                  --target-model <model-id> \
                  --seed <int> \
                  [--dataset-dir /tmp/TRIDENT/dataset] \
                  [--output outputs/run_<ts>.jsonl] \
                  [--judge-a claude-3-5-sonnet-20241022] \
                  [--judge-b gpt-4o-mini] \
                  [--resume]

trident-repro aggregate --input outputs/run_<ts>.jsonl
```

`run` writes one JSON line per prompt as soon as it is scored, so a crash
mid-run leaves a valid partial file. Re-running with `--resume` skips any
prompt `id` already present in the output file.

---

## Output schema (`RunRecord`)

Each line of the output JSONL matches this shape:

```json
{
  "id": "uuid",
  "domain": "law",
  "risk_type": "third_party_dishonesty",
  "ethical_refs": ["Rule 4.1 - Truthfulness in Statements"],
  "harmful_prompt": "...",
  "target_model": "claude-3-5-sonnet-20241022",
  "target_response": "...",
  "judge_a": {"model": "claude-3-5-sonnet-20241022", "score": 1, "reasoning": "..."},
  "judge_b": {"model": "gpt-4o-mini",              "score": 2, "reasoning": "..."},
  "mean_score": 1.5,
  "ts": "2026-04-18T12:34:56Z"
}
```

---

## Aggregation

`trident-repro aggregate --input outputs/run_<ts>.jsonl` prints:

- Per-domain mean harmfulness score.
- Inter-judge **Cohen's kappa** (linear agreement on 1-5 integer scores).
- Inter-judge **Pearson r**.
- Per-domain delta vs. hardcoded TRIDENT Figure 4 published means.

A healthy calibration is **|observed mean - published mean| <= 0.3**.

---

## Project layout

```
src/trident_repro/
    config.py      env + RunConfig
    loader.py      Prompt model; load_jsonl; sample
    models.py      ChatClient Protocol; Anthropic/OpenAI clients; retry
    judge.py       JUDGE_SYSTEM_PROMPT; Judge; Jury
    pipeline.py    run(config) -> Iterator[RunRecord]; crash-safe JSONL
    metrics.py     aggregate, cohen_kappa, pearson_r, compare_to_published
    cli.py         click entry point
tests/             pytest, mock-only (no real API calls)
notebooks/         calibration_check.ipynb (stub)
outputs/           JSONL run files land here
```

---

## Dev loop

```bash
ruff format src tests
ruff check  src tests
mypy
pytest
```

Coverage gate is **70%**; CI should fail below it.

---

## Notes on the jury substitution

TRIDENT's paper uses **Gemma 2-9B** as the second judge. For API-only
reproduction convenience we substitute **GPT-4o-mini**. This changes the
absolute numbers slightly; the *calibration* (within ~0.3 of published
per-model means) is what we check.
