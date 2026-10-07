# QHack 8-Challenge — Validation Results Summary

**Generated:** 2026-06-23T23:01:37

**Benchmark:** 8 QHack challenges. **Test types:** syntactic, semantic, behavioral (per challenge).

Metrics are **means** over all items in the run (QHack: 8 challenges; Qiskit: 10 scoped tasks). Each cell uses the **newest** JSON under `evaluation_results/` for that config and model.

| Metric | Meaning |
|--------|---------|
| **ES** | Executability — tests run without infrastructure failure |
| **CS** | Fraction of oracle-*correct* solutions fully accepted |
| **BDS** | Fraction of oracle-*wrong* solutions rejected |
| **TQS** | Config 1: ES×CS; Configs 2–3: ES×CS×BDS |
| **C_in** | Official input coverage in generated test bodies |
| **CQ** | √(TQS × C_in) |
| **Div** | Test diversity (breadth × coverage) |

---

## Config 1 — Human/canonical solutions only

*Reference (canonical) solution only; TQS = ES × CS.*

| Model | Challenges | ES | CS | BDS | TQS | C_in | CQ | Div |
|-------|----------:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|
| **claudeopus46** | 8 | 1.000 | 0.875 | 0.000 | 0.875 | 0.688 | 0.571 | 0.696 |
| **deepseekv32** | 8 | 0.958 | 0.417 | 0.000 | 0.417 | 0.354 | 0.279 | 0.363 |
| **gemini3pro** | 8 | 1.000 | 0.958 | 0.000 | 0.958 | 0.709 | 0.667 | 0.709 |
| **gpt54** | 8 | 1.000 | 0.833 | 0.000 | 0.833 | 0.709 | 0.584 | 0.709 |
| **qwen3** | 8 | 0.792 | 0.375 | 0.000 | 0.375 | 0.438 | 0.125 | 0.431 |

### Source files (newest JSON per model)

| Model | Generated (local) | Path |
|-------|-------------------|------|
| `claudeopus46` | 2026-05-24T22:48:10 | `evaluation_results/config_1_human_only/claudeopus46/test_quality_results_20260524_224810.json` |
| `deepseekv32` | 2026-05-24T23:02:28 | `evaluation_results/config_1_human_only/deepseekv32/test_quality_results_20260524_230228.json` |
| `gemini3pro` | 2026-05-24T23:17:56 | `evaluation_results/config_1_human_only/gemini3pro/test_quality_results_20260524_231756.json` |
| `gpt54` | 2026-05-24T23:43:29 | `evaluation_results/config_1_human_only/gpt54/test_quality_results_20260524_234329.json` |
| `qwen3` | 2026-05-24T23:59:30 | `evaluation_results/config_1_human_only/qwen3/test_quality_results_20260524_235930.json` |

### Per-model reports

Detailed tables (per challenge/task) are in each model folder:

- **claudeopus46**: `evaluation_results/config_1_human_only/claudeopus46/test_quality_report_*.md` (match timestamp of JSON above)
- **deepseekv32**: `evaluation_results/config_1_human_only/deepseekv32/test_quality_report_*.md` (match timestamp of JSON above)
- **gemini3pro**: `evaluation_results/config_1_human_only/gemini3pro/test_quality_report_*.md` (match timestamp of JSON above)
- **gpt54**: `evaluation_results/config_1_human_only/gpt54/test_quality_report_*.md` (match timestamp of JSON above)
- **qwen3**: `evaluation_results/config_1_human_only/qwen3/test_quality_report_*.md` (match timestamp of JSON above)

---

## Config 2 — Human + LLM labeled cohort

*Human baseline plus oracle-labeled LLM-generated solutions.*

| Model | Challenges | ES | CS | BDS | TQS | C_in | CQ | Div |
|-------|----------:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|
| **claudeopus46** | 8 | 1.000 | 0.883 | 0.802 | 0.685 | 0.688 | 0.548 | 0.696 |
| **deepseekv32** | 8 | 0.958 | 0.467 | 0.750 | 0.258 | 0.354 | 0.268 | 0.363 |
| **gemini3pro** | 8 | 1.000 | 0.958 | 0.667 | 0.625 | 0.709 | 0.625 | 0.709 |
| **gpt54** | 8 | 1.000 | 0.842 | 0.709 | 0.550 | 0.709 | 0.560 | 0.709 |
| **qwen3** | 8 | 0.792 | 0.375 | 0.500 | 0.083 | 0.438 | 0.083 | 0.431 |

### Oracle probe pool (aggregated over all items in run)

| Model | Total probes | Correct | Wrong | Unknown |
|-------|-------------:|--------:|------:|--------:|
| claudeopus46 | 64 | 25 | 29 | 10 |
| deepseekv32 | 64 | 25 | 29 | 10 |
| gemini3pro | 64 | 25 | 29 | 10 |
| gpt54 | 64 | 25 | 29 | 10 |
| qwen3 | 64 | 25 | 29 | 10 |

### Source files (newest JSON per model)

| Model | Generated (local) | Path |
|-------|-------------------|------|
| `claudeopus46` | 2026-05-25T00:31:30 | `evaluation_results/config_2_llm_cohort/claudeopus46/test_quality_results_20260525_003130.json` |
| `deepseekv32` | 2026-05-25T08:46:08 | `evaluation_results/config_2_llm_cohort/deepseekv32/test_quality_results_20260525_084608.json` |
| `gemini3pro` | 2026-05-25T10:07:43 | `evaluation_results/config_2_llm_cohort/gemini3pro/test_quality_results_20260525_100743.json` |
| `gpt54` | 2026-05-25T10:41:50 | `evaluation_results/config_2_llm_cohort/gpt54/test_quality_results_20260525_104150.json` |
| `qwen3` | 2026-05-25T11:06:03 | `evaluation_results/config_2_llm_cohort/qwen3/test_quality_results_20260525_110603.json` |

### Per-model reports

Detailed tables (per challenge/task) are in each model folder:

- **claudeopus46**: `evaluation_results/config_2_llm_cohort/claudeopus46/test_quality_report_*.md` (match timestamp of JSON above)
- **deepseekv32**: `evaluation_results/config_2_llm_cohort/deepseekv32/test_quality_report_*.md` (match timestamp of JSON above)
- **gemini3pro**: `evaluation_results/config_2_llm_cohort/gemini3pro/test_quality_report_*.md` (match timestamp of JSON above)
- **gpt54**: `evaluation_results/config_2_llm_cohort/gpt54/test_quality_report_*.md` (match timestamp of JSON above)
- **qwen3**: `evaluation_results/config_2_llm_cohort/qwen3/test_quality_report_*.md` (match timestamp of JSON above)

---

## Config 3 — Human + synthetic wrong negatives

*Human baseline plus oracle-validated synthetic wrong probes.*

| Model | Challenges | ES | CS | BDS | TQS | C_in | CQ | Div |
|-------|----------:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|
| **claudeopus46** | 8 | 1.000 | 0.875 | 0.834 | 0.709 | 0.688 | 0.530 | 0.696 |
| **deepseekv32** | 8 | 0.958 | 0.417 | 0.750 | 0.250 | 0.354 | 0.250 | 0.363 |
| **gemini3pro** | 8 | 1.000 | 0.958 | 0.667 | 0.625 | 0.709 | 0.625 | 0.709 |
| **gpt54** | 8 | 1.000 | 0.833 | 0.709 | 0.542 | 0.709 | 0.542 | 0.709 |
| **qwen3** | 8 | 0.792 | 0.375 | 0.500 | 0.083 | 0.438 | 0.083 | 0.431 |

### Oracle probe pool (aggregated over all items in run)

| Model | Total probes | Correct | Wrong | Unknown |
|-------|-------------:|--------:|------:|--------:|
| claudeopus46 | 8 | 0 | 8 | 0 |
| deepseekv32 | 8 | 0 | 8 | 0 |
| gemini3pro | 8 | 0 | 8 | 0 |
| gpt54 | 8 | 0 | 8 | 0 |
| qwen3 | 8 | 0 | 8 | 0 |

### Source files (newest JSON per model)

| Model | Generated (local) | Path |
|-------|-------------------|------|
| `claudeopus46` | 2026-05-25T11:45:20 | `evaluation_results/config_3_synthetic/claudeopus46/test_quality_results_20260525_114520.json` |
| `deepseekv32` | 2026-05-25T12:30:22 | `evaluation_results/config_3_synthetic/deepseekv32/test_quality_results_20260525_123022.json` |
| `gemini3pro` | 2026-05-25T13:41:40 | `evaluation_results/config_3_synthetic/gemini3pro/test_quality_results_20260525_134140.json` |
| `gpt54` | 2026-05-25T14:16:20 | `evaluation_results/config_3_synthetic/gpt54/test_quality_results_20260525_141620.json` |
| `qwen3` | 2026-05-25T14:39:20 | `evaluation_results/config_3_synthetic/qwen3/test_quality_results_20260525_143920.json` |

### Per-model reports

Detailed tables (per challenge/task) are in each model folder:

- **claudeopus46**: `evaluation_results/config_3_synthetic/claudeopus46/test_quality_report_*.md` (match timestamp of JSON above)
- **deepseekv32**: `evaluation_results/config_3_synthetic/deepseekv32/test_quality_report_*.md` (match timestamp of JSON above)
- **gemini3pro**: `evaluation_results/config_3_synthetic/gemini3pro/test_quality_report_*.md` (match timestamp of JSON above)
- **gpt54**: `evaluation_results/config_3_synthetic/gpt54/test_quality_report_*.md` (match timestamp of JSON above)
- **qwen3**: `evaluation_results/config_3_synthetic/qwen3/test_quality_report_*.md` (match timestamp of JSON above)

---

## How to refresh this file

From the repository root (after new evaluation runs):

```powershell
python build_evaluation_results_summary.py
```
