# Qiskit HumanEval — automatic test generation and evaluation (standalone)

This folder is **separate from the PennyLane QHack** pipeline. It adapts the same research idea:

1. **Generate tests** with an LLM using the **task prompt / stub only** (no canonical solution in the generation prompt).
2. **Evaluate tests** by executing them against **known solutions**: canonical human baseline, optional LLM-generated solutions (oracle-labelled), and optional synthetic wrong mutants.

Dataset: [qiskit-community/qiskit-human-eval](https://github.com/qiskit-community/qiskit-human-eval) (paper: arXiv:2406.14712).

Related NYUAD work (QHack): [MeriemTerki/NYUAD-Research-Quantum-Code-Evaluation](https://github.com/MeriemTerki/NYUAD-Research-Quantum-Code-Evaluation/tree/correctness-coverage-8-Qhack-challenges).

## Layout

| Path | Role |
|------|------|
| `datasets/` | `dataset_qiskit_test_human_eval.json` (full) and `*_hard.json` |
| `Framework_Qiskit_Human_Eval/` | Materialized tasks after `prepare` (`full/`, `hard/`) |
| `config.py` | OpenRouter models + API key from `.env` |
| `openrouter_client.py` | Shared OpenRouter caller (no dependency on QHack `generate_tests.py`) |
| `prepare_qiskit_human_eval.py` | JSON → `tasks/`, `Human_solutions/canonical/`, `official_check.py` |
| `generate_tests_qiskit_he.py` | LLM → `generated_tests/*/test_{syntactic,semantic,behavioral}.py` |
| `generate_llm_solutions_qiskit_he.py` | Optional: LLM solutions under `LLM_generated_solutions/` |
| `evaluate_qiskit_he.py` | ES, CS, BDS, TQS, coverage-style metrics |
| `oracle_qiskit_he.py` | Official `check(candidate)` oracle |
| `evaluate_solutions.py` | Shared scoring helpers (same role as in QHack) |
| `challenge_mapper.py` | Required by `evaluate_solutions.py` import graph (QHack discovery; unused by Qiskit HE paths) |
| `Framework_Qiskit_Human_Eval/full/evaluation_scope_tasks.txt` | Optional fixed task list for **research runs** (use with `--scoped`) |

**Research model set (examples below):** `claudeopus46`, `deepseekv32`, `gemini3pro`, `gpt54`, `qwen3` — pass them to `--models` in that order for generation; evaluate once per model with `--test-gen-model`.

## Dataset shapes (important)

- **full** (`dataset_qiskit_test_human_eval.json`): `prompt` = imports + function stub; `canonical_solution` = **body only**. The prepared `reference_solution.py` is **prompt + body** (full runnable module).
- **hard** (`dataset_qiskit_test_human_eval_hard.json`): natural-language `prompt`; `canonical_solution` is already a **full module**.

## Setup

```bash
cd Qiskit_HumanEval_Framework
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
copy .env.example .env   # put OPENROUTER_API_KEY=
```

## 1) Materialize tasks

```bash
python prepare_qiskit_human_eval.py --only-variant full
python oracle_qiskit_he.py --root ./Framework_Qiskit_Human_Eval/full --limit 3
```

## 2) Fixed 10-task scope (recommended for papers)

1. Edit `Framework_Qiskit_Human_Eval/full/evaluation_scope_tasks.txt` (one `task_NNNN` per line), or copy from `evaluation_scope_tasks.example.txt`.
2. Generate **within that pool** with stratification (3 easy + 3 intermediate + 3 hard + 1 any):

```bash
python generate_tests_qiskit_he.py --root ./Framework_Qiskit_Human_Eval/full --scoped --stratify 3,3,3,1 --models claudeopus46 deepseekv32 gemini3pro gpt54 qwen3
```

3. Evaluate **only those tasks** (same file), **once per test generator** (each model writes under `generated_tests/<task>/<model>/`):

```powershell
$models = 'claudeopus46','deepseekv32','gemini3pro','gpt54','qwen3'
foreach ($m in $models) {
  python evaluate_qiskit_he.py --root ./Framework_Qiskit_Human_Eval/full --scoped --human-only --use-synthetic-negatives --n-synthetic-negatives 3 --test-gen-model $m
}
```

Single model (example: `deepseekv32` only):

```bash
python evaluate_qiskit_he.py --root ./Framework_Qiskit_Human_Eval/full --scoped --human-only --use-synthetic-negatives --n-synthetic-negatives 3 --test-gen-model deepseekv32
```

Alternatives: `--only task_0000 task_0001 …` or `--only-file path/to/tasks.txt` (same line format).  
**Do not** average metrics over all 151 tasks unless you generated tests for every task.

## 2b) Generate tests without a scope file (full corpus or ad-hoc)

Uses difficulty labels `basic` / `intermediate` / `difficult` from the JSON.

```bash
python generate_tests_qiskit_he.py --root ./Framework_Qiskit_Human_Eval/full --model deepseekv32 --stratify 3,3,3,1
```

Multi-model (research set):

```bash
python generate_tests_qiskit_he.py --root ./Framework_Qiskit_Human_Eval/full --stratify 3,3,3,1 --models claudeopus46 deepseekv32 gemini3pro gpt54 qwen3
```

Generation prompts use **`prompt.txt`** (stub + description) only; the canonical answer is **not** shown to the LLM.  
For evaluation-focused studies, generation is intentionally **single-pass** (no canonical-pass optimization and no synthetic-negative repair during generation).

## 3) (Optional) Generate LLM solutions for BDS

```bash
python generate_llm_solutions_qiskit_he.py --root ./Framework_Qiskit_Human_Eval/full --scoped --model deepseekv32 --label-oracle
```

Files go to `LLM_generated_solutions/<model>/task_NNNN/generated_non_rag_1.py`. The evaluator oracle-labels them when you run evaluation **without** `--human-only`.

## 4) Evaluate generated tests

**Human baseline + synthetic wrong probes** (scoped to `evaluation_scope_tasks.txt`). Loop over all five generators:

```powershell
$models = 'claudeopus46','deepseekv32','gemini3pro','gpt54','qwen3'
foreach ($m in $models) {
  python evaluate_qiskit_he.py --root ./Framework_Qiskit_Human_Eval/full --scoped --human-only --use-synthetic-negatives --n-synthetic-negatives 3 --test-gen-model $m
}
```

Without `--scoped`, evaluation iterates **all** tasks in `tasks/` (missing tests → ES=0). Prefer `--scoped` or explicit `--only`.

**With LLM solution pool** (drop `--human-only`; keep `--scoped`; set `--llm-models` to whichever solution folders you have):

```powershell
$models = 'claudeopus46','deepseekv32','gemini3pro','gpt54','qwen3'
foreach ($m in $models) {
  python evaluate_qiskit_he.py --root ./Framework_Qiskit_Human_Eval/full --scoped --test-gen-model $m --llm-models claudeopus46 deepseekv32 gemini3pro gpt54 qwen3
}
```

Only evaluate tasks that actually have generated tests for `--test-gen-model`; otherwise you will see `Test file does not exist` for missing tasks.

## 5) One-shot: generate + evaluate (scoped)

`run_pipeline_qiskit_he.py` runs **one** test generator then evaluates it. For the full five-model study, generate with `generate_tests_qiskit_he.py --models …` (above), then evaluate with the loop. Quick check with a single model:

```bash
python run_pipeline_qiskit_he.py --root ./Framework_Qiskit_Human_Eval/full --test-gen-model claudeopus46 --scoped --stratify 3,3,3,1 --human-only --use-synthetic-negatives --n-synthetic-negatives 3
```

## Packaging as a zip

From the parent of this folder:

```powershell
Compress-Archive -Path Qiskit_HumanEval_Framework -DestinationPath Qiskit_HumanEval_Framework.zip -Force
```
