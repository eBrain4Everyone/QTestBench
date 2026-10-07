# Qiskit HumanEval — Validation Results Summary

**Generated:** 2026-06-23T23:01:37

**Benchmark:** 10-task scoped slice (`evaluation_scope_tasks.txt`). **Configs 1–3** match the validation pipeline in `VALIDATION_EVALUATION.md`.

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

| Model | Tasks | ES | CS | BDS | TQS | C_in | CQ | Div |
|-------|----------:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|
| **claudeopus46** | 10 | 1.000 | 0.767 | 0.000 | 0.767 | 0.364 | 0.283 | 0.377 |
| **deepseekv32** | 10 | 1.000 | 0.300 | 0.000 | 0.300 | 0.372 | 0.129 | 0.385 |
| **gemini3pro** | 10 | 1.000 | 0.700 | 0.000 | 0.700 | 0.328 | 0.239 | 0.355 |
| **gpt54** | 10 | 1.000 | 0.466 | 0.000 | 0.466 | 0.326 | 0.163 | 0.353 |
| **qwen3** | 10 | 0.933 | 0.300 | 0.000 | 0.300 | 0.257 | 0.159 | 0.297 |

### Source files (newest JSON per model)

| Model | Generated (local) | Path |
|-------|-------------------|------|
| `claudeopus46` | 2026-05-25T18:17:55 | `evaluation_results/config_1_human_only/claudeopus46/test_quality_results_qiskit_he_20260525_181755.json` |
| `deepseekv32` | 2026-05-25T18:21:48 | `evaluation_results/config_1_human_only/deepseekv32/test_quality_results_qiskit_he_20260525_182148.json` |
| `gemini3pro` | 2026-05-25T18:28:10 | `evaluation_results/config_1_human_only/gemini3pro/test_quality_results_qiskit_he_20260525_182810.json` |
| `gpt54` | 2026-05-25T18:36:30 | `evaluation_results/config_1_human_only/gpt54/test_quality_results_qiskit_he_20260525_183630.json` |
| `qwen3` | 2026-05-25T18:41:09 | `evaluation_results/config_1_human_only/qwen3/test_quality_results_qiskit_he_20260525_184109.json` |

### Per-model reports

Detailed tables (per challenge/task) are in each model folder:

- **claudeopus46**: `evaluation_results/config_1_human_only/claudeopus46/test_quality_report_qiskit_he_*.md` (match timestamp of JSON above)
- **deepseekv32**: `evaluation_results/config_1_human_only/deepseekv32/test_quality_report_qiskit_he_*.md` (match timestamp of JSON above)
- **gemini3pro**: `evaluation_results/config_1_human_only/gemini3pro/test_quality_report_qiskit_he_*.md` (match timestamp of JSON above)
- **gpt54**: `evaluation_results/config_1_human_only/gpt54/test_quality_report_qiskit_he_*.md` (match timestamp of JSON above)
- **qwen3**: `evaluation_results/config_1_human_only/qwen3/test_quality_report_qiskit_he_*.md` (match timestamp of JSON above)

---

## Config 2 — Human + LLM labeled cohort

*Human baseline plus oracle-labeled LLM-generated solutions.*

| Model | Tasks | ES | CS | BDS | TQS | C_in | CQ | Div |
|-------|----------:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|
| **claudeopus46** | 10 | 1.000 | 0.839 | 0.453 | 0.326 | 0.364 | 0.188 | 0.377 |
| **deepseekv32** | 10 | 1.000 | 0.424 | 0.513 | 0.114 | 0.372 | 0.051 | 0.385 |
| **gemini3pro** | 10 | 1.000 | 0.819 | 0.523 | 0.369 | 0.328 | 0.133 | 0.355 |
| **gpt54** | 10 | 1.000 | 0.573 | 0.503 | 0.153 | 0.326 | 0.098 | 0.353 |
| **qwen3** | 10 | 0.933 | 0.366 | 0.595 | 0.249 | 0.257 | 0.126 | 0.297 |

### Oracle probe pool (aggregated over all items in run)

| Model | Total probes | Correct | Wrong | Unknown |
|-------|-------------:|--------:|------:|--------:|
| claudeopus46 | 199 | 119 | 80 | 0 |
| deepseekv32 | 199 | 119 | 80 | 0 |
| gemini3pro | 199 | 119 | 80 | 0 |
| gpt54 | 199 | 119 | 80 | 0 |
| qwen3 | 199 | 119 | 80 | 0 |

### Source files (newest JSON per model)

| Model | Generated (local) | Path |
|-------|-------------------|------|
| `claudeopus46` | 2026-06-23T20:22:16 | `evaluation_results/config_2_llm_cohort/claudeopus46/test_quality_results_qiskit_he_20260623_202216.json` |
| `deepseekv32` | 2026-06-23T20:53:02 | `evaluation_results/config_2_llm_cohort/deepseekv32/test_quality_results_qiskit_he_20260623_205302.json` |
| `gemini3pro` | 2026-06-23T21:21:53 | `evaluation_results/config_2_llm_cohort/gemini3pro/test_quality_results_qiskit_he_20260623_212153.json` |
| `gpt54` | 2026-06-23T22:03:58 | `evaluation_results/config_2_llm_cohort/gpt54/test_quality_results_qiskit_he_20260623_220358.json` |
| `qwen3` | 2026-06-23T22:55:29 | `evaluation_results/config_2_llm_cohort/qwen3/test_quality_results_qiskit_he_20260623_225529.json` |

### Per-model reports

Detailed tables (per challenge/task) are in each model folder:

- **claudeopus46**: `evaluation_results/config_2_llm_cohort/claudeopus46/test_quality_report_qiskit_he_*.md` (match timestamp of JSON above)
- **deepseekv32**: `evaluation_results/config_2_llm_cohort/deepseekv32/test_quality_report_qiskit_he_*.md` (match timestamp of JSON above)
- **gemini3pro**: `evaluation_results/config_2_llm_cohort/gemini3pro/test_quality_report_qiskit_he_*.md` (match timestamp of JSON above)
- **gpt54**: `evaluation_results/config_2_llm_cohort/gpt54/test_quality_report_qiskit_he_*.md` (match timestamp of JSON above)
- **qwen3**: `evaluation_results/config_2_llm_cohort/qwen3/test_quality_report_qiskit_he_*.md` (match timestamp of JSON above)

---

## Config 3 — Human + synthetic wrong negatives

*Human baseline plus oracle-validated synthetic wrong probes.*

| Model | Tasks | ES | CS | BDS | TQS | C_in | CQ | Div |
|-------|----------:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|
| **claudeopus46** | 10 | 1.000 | 0.767 | 0.456 | 0.289 | 0.364 | 0.067 | 0.377 |
| **deepseekv32** | 10 | 1.000 | 0.333 | 0.522 | 0.056 | 0.372 | 0.027 | 0.385 |
| **gemini3pro** | 10 | 1.000 | 0.700 | 0.544 | 0.345 | 0.328 | 0.086 | 0.355 |
| **gpt54** | 10 | 1.000 | 0.466 | 0.478 | 0.144 | 0.326 | 0.054 | 0.353 |
| **qwen3** | 10 | 0.933 | 0.300 | 0.561 | 0.161 | 0.257 | 0.080 | 0.297 |

### Oracle probe pool (aggregated over all items in run)

| Model | Total probes | Correct | Wrong | Unknown |
|-------|-------------:|--------:|------:|--------:|
| claudeopus46 | 12 | 0 | 12 | 0 |
| deepseekv32 | 12 | 0 | 12 | 0 |
| gemini3pro | 13 | 0 | 13 | 0 |
| gpt54 | 13 | 0 | 13 | 0 |
| qwen3 | 12 | 0 | 12 | 0 |

### Source files (newest JSON per model)

| Model | Generated (local) | Path |
|-------|-------------------|------|
| `claudeopus46` | 2026-05-25T20:03:56 | `evaluation_results/config_3_synthetic/claudeopus46/test_quality_results_qiskit_he_20260525_200356.json` |
| `deepseekv32` | 2026-05-25T20:13:05 | `evaluation_results/config_3_synthetic/deepseekv32/test_quality_results_qiskit_he_20260525_201305.json` |
| `gemini3pro` | 2026-05-25T20:37:35 | `evaluation_results/config_3_synthetic/gemini3pro/test_quality_results_qiskit_he_20260525_203735.json` |
| `gpt54` | 2026-05-25T20:44:12 | `evaluation_results/config_3_synthetic/gpt54/test_quality_results_qiskit_he_20260525_204412.json` |
| `qwen3` | 2026-05-25T20:47:40 | `evaluation_results/config_3_synthetic/qwen3/test_quality_results_qiskit_he_20260525_204740.json` |

### Per-model reports

Detailed tables (per challenge/task) are in each model folder:

- **claudeopus46**: `evaluation_results/config_3_synthetic/claudeopus46/test_quality_report_qiskit_he_*.md` (match timestamp of JSON above)
- **deepseekv32**: `evaluation_results/config_3_synthetic/deepseekv32/test_quality_report_qiskit_he_*.md` (match timestamp of JSON above)
- **gemini3pro**: `evaluation_results/config_3_synthetic/gemini3pro/test_quality_report_qiskit_he_*.md` (match timestamp of JSON above)
- **gpt54**: `evaluation_results/config_3_synthetic/gpt54/test_quality_report_qiskit_he_*.md` (match timestamp of JSON above)
- **qwen3**: `evaluation_results/config_3_synthetic/qwen3/test_quality_report_qiskit_he_*.md` (match timestamp of JSON above)

---

## How to refresh this file

From the repository root (after new evaluation runs):

```powershell
python build_evaluation_results_summary.py
```
