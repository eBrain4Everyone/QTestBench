# Qiskit HumanEval — Test Generation & Evaluation Summary

This document summarizes **how** tests were generated and evaluated in the Qiskit HumanEval framework, and **how to interpret** the metrics for the **latest scoped 10-task runs**.

---

## 1. Scope of the experiment

- **Corpus slice:** A **fixed list of 10 tasks** (stratified difficulty), not the full HumanEval set (~151 tasks).
- **Configuration file:** `evaluation_scope_tasks.txt` in this folder lists the task IDs (e.g. `task_0000`, …). The scripts use **`--scoped`** so generation and evaluation both target **the same** tasks.
- **Purpose:** Comparable metrics across models without dilution from tasks with missing or partial test files.

---

## 2. How test generation was done

**Script:** `generate_tests_qiskit_he.py` (from the `Qiskit_HumanEval_Framework` directory).

**Mechanism:**

1. For each scoped task, an **LLM** (via OpenRouter) generates **three** pytest modules:
   - `test_syntactic.py` — structure / import / callable checks (lightweight).
   - `test_semantic.py` — quantum semantics (statevectors, operators, etc., as appropriate).
   - `test_behavioral.py` — end-to-end behavior (possibly simulators, small shots).

2. Each file is written under:

   `generated_tests/<task_name>/<model_key>/`

3. **Prompting** encodes the harness: tests load the candidate from `builtins` (`INJECTED_SOLUTION_CODE`, `INJECTED_ENTRY_POINT`) and must not paste the full solution into the test file.

4. **Generation mode used in this study (evaluation-first):**
   - Test generation is **single-pass** per test type (syntactic / semantic / behavioral).
   - No generation-time canonical-pass optimization loop.
   - No generation-time synthetic-negative repair loop.
   - This preserves a clean separation: generation creates candidate tests, evaluation measures quality.

**Models compared (example run):**

| Model key      | Role                          |
|----------------|-------------------------------|
| `claudeopus46` | Anthropic Claude              |
| `deepseekv32`  | DeepSeek                      |
| `gemini3pro`   | Google Gemini                 |
| `gpt54`        | OpenAI GPT                    |
| `qwen3`        | Qwen                          |

**Generation command used** (from `Qiskit_HumanEval_Framework`, scoped root):

```powershell
python generate_tests_qiskit_he.py --root .\Framework_Qiskit_Human_Eval\full --scoped --model <MODEL_KEY>
```

**Resume:** Checkpoints `generation_checkpoint_qiskit_he_<model>.json` record progress so runs can be resumed.

---

## 3. Validation configurations (Configs 1–3)

All scoped evaluations use the same three **alternative** cohorts (not a sequential pipeline):

| Config | Directory | Cohort | Qiskit command flags |
|--------|-----------|--------|----------------------|
| **1** | `evaluation_results/config_1_human_only/<model>/` | Canonical human solution only | `--validation-config 1` or `--scoped --human-only` |
| **2** | `evaluation_results/config_2_llm_cohort/<model>/` | Human + oracle-labeled LLM solutions | `--validation-config 2` or `--scoped` (default pool) |
| **3** | `evaluation_results/config_3_synthetic/<model>/` | Human + synthetic wrong negatives | `--validation-config 3` or `--scoped --human-only --use-synthetic-negatives` |

**Orchestration (both frameworks):** from the repository root,

```powershell
# Run only missing model×config JSON results, then refresh markdown headers
python run_validation_evaluations.py

# Refresh markdown from existing JSON only
python refresh_validation_reports.py
```

Legacy folder names (`config_a_trusted_correct`, `config_b_llm_cohort`, `config_c_synthetic_calibration`) are still recognized when refreshing reports.

---

## 4. How evaluation was done

**Script:** `evaluate_qiskit_he.py`.

**Mechanism:**

1. For each task in scope, load the **generated** tests for the chosen **`--test-gen-model`**.

2. **Executability (ES):** Run the test file against injected solutions; check whether pytest runs without infrastructure/syntax failure.

3. **Correctness score (CS):** Measure how often **correct** reference / trusted solutions are **accepted** (tests should pass). Low CS means **false failures** — tests that reject valid implementations.

4. **Bug-detection score (BDS):** Measure how often **incorrect** solutions are **rejected** (tests should fail). The framework can include:
   - **Synthetic negatives:** Small **mutations** of the canonical solution that the **dataset oracle** labels as **wrong** (e.g. `return None`, flip `==`, swap a gate). Tests are run with these mutants injected; if a known-bad program still passes all tests, BDS is reduced.

5. **Test quality score (TQS):** Combines ES, CS, and BDS (conceptually: all three must be strong for a high score).

6. **Coverage of oracle literals (C_in) and composite quality (CQ):** Compare generated assertions to strings extracted from `official_check.py`; **CQ** blends TQS with this coverage. Low **C_in** often means tests do not literally echo oracle strings — that is **not** the same as “tests are useless,” but it explains modest **CQ** even when TQS is moderate.

**Example evaluation command** (per model, scoped):

```powershell
python evaluate_qiskit_he.py --root .\Framework_Qiskit_Human_Eval\full --scoped `
  --test-gen-model <MODEL_KEY> --use-synthetic-negatives --n-synthetic-negatives 5
```

**Outputs:** JSON reports under `evaluation_results/`, e.g. `test_quality_results_qiskit_he_<timestamp>.json`.

---

## 5. Results — latest scoped runs (10 tasks each)

The three validation configurations should be interpreted separately:

### 5.1 Config 1 — Human/canonical solutions only (trusted-correct baseline)

Representative reports (newest JSON):
- `test_quality_results_qiskit_he_20260525_181755.json` (`claudeopus46`)
- `test_quality_results_qiskit_he_20260525_182148.json` (`deepseekv32`)
- `test_quality_results_qiskit_he_20260525_182810.json` (`gemini3pro`)
- `test_quality_results_qiskit_he_20260525_183630.json` (`gpt54`)
- `test_quality_results_qiskit_he_20260525_184109.json` (`qwen3`)

| Model | Mean ES | Mean CS | Mean BDS | Mean TQS | Mean CQ | Mean C_in |
|-------|---------|---------|----------|----------|---------|------------|
| claudeopus46 | 1.000 | **0.767** | 0.000 | **0.767** | **0.283** | 0.364 |
| deepseekv32  | 1.000 | 0.300 | 0.000 | 0.300 | 0.129 | **0.372** |
| gemini3pro   | 1.000 | 0.700 | 0.000 | 0.700 | 0.239 | 0.328 |
| gpt54        | 1.000 | 0.466 | 0.000 | 0.466 | 0.163 | 0.326 |
| qwen3        | 0.933 | 0.300 | 0.000 | 0.300 | 0.159 | 0.257 |

---

### 5.2 Config 2 (LLM cohort) — Human + oracle-labeled LLM solution pool

Command pattern:

```powershell
python evaluate_qiskit_he.py --root .\Framework_Qiskit_Human_Eval\full --scoped `
  --test-gen-model <MODEL_KEY> --llm-models claudeopus46 deepseekv32 gemini3pro gpt54 qwen3
```

Reports:
- `test_quality_results_qiskit_he_20260530_185443.json` (`claudeopus46`)
- `test_quality_results_qiskit_he_20260530_191336.json` (`deepseekv32`)
- `test_quality_results_qiskit_he_20260530_192624.json` (`gemini3pro`)
- `test_quality_results_qiskit_he_20260530_195944.json` (`gpt54`)
- `test_quality_results_qiskit_he_20260530_202009.json` (`qwen3`)

| Model | Mean ES | Mean CS | Mean BDS | Mean TQS | Mean CQ | Mean C_in |
|-------|---------|---------|----------|----------|---------|------------|
| claudeopus46 | 1.000 | **0.822** | 0.111 | **0.078** | **0.053** | 0.364 |
| deepseekv32  | 1.000 | 0.422 | 0.133 | 0.000 | 0.000 | **0.372** |
| gemini3pro   | 1.000 | 0.797 | 0.111 | 0.033 | 0.000 | 0.328 |
| gpt54        | 1.000 | 0.555 | 0.133 | 0.000 | 0.000 | 0.326 |
| qwen3        | 0.933 | 0.356 | 0.133 | 0.033 | 0.000 | 0.257 |

Observed probe-label mix in this track (per model run, aggregated over 10 tasks): **50** total probes = **30 correct**, **4 wrong**, **16 unknown**.

### 5.3 Config 3 (synthetic calibration) — Human baseline + synthetic negatives

Command pattern:

```powershell
python evaluate_qiskit_he.py --root .\Framework_Qiskit_Human_Eval\full --scoped `
  --human-only --use-synthetic-negatives --n-synthetic-negatives 3 --test-gen-model <MODEL_KEY>
```

Reports:
- `test_quality_results_qiskit_he_20260525_200356.json` (`claudeopus46`)
- `test_quality_results_qiskit_he_20260525_201305.json` (`deepseekv32`)
- `test_quality_results_qiskit_he_20260525_203735.json` (`gemini3pro`)
- `test_quality_results_qiskit_he_20260525_204412.json` (`gpt54`)
- `test_quality_results_qiskit_he_20260525_204740.json` (`qwen3`)

| Model | Mean ES | Mean CS | Mean BDS | Mean TQS | Mean CQ | Mean C_in |
|-------|---------|---------|----------|----------|---------|------------|
| gemini3pro   | 1.000 | 0.700 | 0.544 | **0.345** | **0.086** | 0.328 |
| claudeopus46 | 1.000 | **0.767** | 0.456 | 0.289 | 0.067 | 0.364 |
| qwen3        | 0.933 | 0.300 | **0.561** | 0.161 | 0.080 | 0.257 |
| gpt54        | 1.000 | 0.466 | 0.478 | 0.144 | 0.054 | 0.326 |
| deepseekv32  | 1.000 | 0.333 | 0.522 | 0.056 | 0.027 | **0.372** |

Observed probe-label mix in this configuration: synthetic negatives dominate; per model run totals were about **11-13 probes**, all oracle-labelled **wrong** (expected in this setup).

**Per-type pattern (typical):** semantic tests are often stronger on CS than purely syntactic tests; syntactic tests can still miss semantic bugs and depress BDS. Individual JSON files contain `scores_by_type` for exact breakdowns.

**Spread:** task-level quality remains uneven (several tasks at `avg_tqs=0` in Config 2, with isolated high-TQS tasks in all configurations).

---

## 6. Interpretation — quality of the generated tests

### 6.1 Overall assessment

Under this pipeline and metric definition, generated tests show **mixed quality**, and interpretation depends on configuration:

- **Config 2 (LLM solution pool):** very low BDS (~0.11–0.13) and compressed TQS (0.00–0.078).  
  Main reason: very few oracle-wrong LLM probes (only 4 wrong among 50), plus many unknown labels; discrimination signal is weak in this snapshot.

- **Config 3 (human + synthetic negatives):** BDS improves clearly (~0.46–0.56) and TQS separates models better (0.056–0.345).  
  This is expected because synthetic wrong probes are controlled and plentiful.

- **CS remains below 1.0** in all configurations, indicating false negatives still occur (some valid behavior is rejected).

- **ES is mostly stable** (usually 1.0; qwen3 at 0.933), so infrastructure executability is not the primary bottleneck.

### 6.2 Ranking (this batch)

By **mean TQS** (latest runs):

- **Config 1 (human only):** `claudeopus46` > `gemini3pro` > `gpt54` > (`deepseekv32` ~= `qwen3`).
- **Config 2 (LLM cohort):** `claudeopus46` > (`gemini3pro` ~= `qwen3`) > (`deepseekv32` ~= `gpt54`).
- **Config 3 (synthetic):** `gemini3pro` > `claudeopus46` > `qwen3` > `gpt54` > `deepseekv32`.

By **mean CS**, `claudeopus46` is strongest in all three configurations.

### 6.3 What you can claim in writing

- **Fair comparison:** same 10 tasks, same harness, same scoring code; model differences are meaningful within each track.

- **Report the three configurations separately:** Config 1 (trusted baseline), Config 2 (LLM-pool transfer), and Config 3 (synthetic calibration) answer different questions and should not be merged into one score.

- **Limited generalization:** results apply to the scoped 10-task slice; larger coverage may shift absolute values and ranking.

- **Quality statement:** tests are executable and partially discriminative, with better bug-detection signal under controlled synthetic probes than under the current LLM probe pool.

---

## 7. Synthetic negatives (short reference)

**Synthetic negatives** are **mutants** of the canonical solution that the **official oracle** marks as **wrong**. Evaluation runs the **same generated tests** with these mutants injected as the “solution.” If tests **pass** on a known-bad mutant, **BDS** suffers — that is intentional: it measures whether the suite **detects** obvious breakage.

Implementation details: `evaluate_qiskit_he.py` — `build_synthetic_negative_candidates`, `make_synthetic_wrong_solutions`.

---

## 8. File locations (this framework tree)

| Artifact              | Location |
|-----------------------|----------|
| Scoped task list      | `evaluation_scope_tasks.txt` |
| Generated tests       | `generated_tests/` |
| Generation checkpoints| `generation_checkpoint_qiskit_he_<model>.json` |
| Evaluation JSON       | `evaluation_results/test_quality_results_qiskit_he_*.json` |

---

*Generated for documentation of the Qiskit HumanEval scoped evaluation workflow. Update the results table if you add new evaluation JSON files or change scope.*
