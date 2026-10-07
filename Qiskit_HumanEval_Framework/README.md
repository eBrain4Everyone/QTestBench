# Qiskit HumanEval Framework

How to **prepare tasks**, **generate tests**, and **run** QTestBench evaluation on Qiskit HumanEval.

Parent overview: [root README](../README.md).

---

## Goals of this folder

1. Materialize HumanEval tasks into runnable folders.
2. Ask an LLM to write pytest suites (`syntactic`, `semantic`, `behavioral`).
3. **Run those tests** against candidate solutions and score them with the official `check(candidate)` oracle.

Generation prompts use the task prompt/stub only (canonical solution is withheld).

---

## Setup

```bash
cd Qiskit_HumanEval_Framework
python -m venv venv
venv\Scripts\activate          # Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`:

```text
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

Never commit `.env`.

---

## How to run the tests (paper protocol)

Reported paper results use a **fixed 10-task scope**:

```text
Framework_Qiskit_Human_Eval/full/evaluation_scope_tasks.txt
```

Always prefer `--scoped` for paper-comparable runs.

### Step 1 - Materialize tasks (once)

```bash
python prepare_qiskit_human_eval.py --only-variant full
```

Optional oracle smoke test:

```bash
python oracle_qiskit_he.py --root ./Framework_Qiskit_Human_Eval/full --limit 3
```

### Step 2 - Generate pytest modules

```bash
python generate_tests_qiskit_he.py \
  --root ./Framework_Qiskit_Human_Eval/full \
  --scoped \
  --models claudeopus46
```

Multi-model paper set:

```bash
python generate_tests_qiskit_he.py \
  --root ./Framework_Qiskit_Human_Eval/full \
  --scoped \
  --models claudeopus46 deepseekv32 gemini3pro gpt54 qwen3
```

Generated files:

```text
Framework_Qiskit_Human_Eval/full/generated_tests/<task>/<model>/
  test_syntactic.py
  test_semantic.py
  test_behavioral.py
```

### Step 3 - Run and score the generated tests

This is the main command to **run the tests** for Qiskit:

```bash
python evaluate_qiskit_he.py \
  --root ./Framework_Qiskit_Human_Eval/full \
  --scoped \
  --human-only \
  --use-synthetic-negatives \
  --n-synthetic-negatives 3 \
  --test-gen-model claudeopus46
```

What this does:

1. Loads generated pytest suites for the scoped tasks.
2. Injects the trusted baseline (and optional probes).
3. Runs pytest.
4. Labels probes with the official checker.
5. Writes ES/CS/BDS/TQS reports under `evaluation_results/`.

Repeat with `--test-gen-model <name>` for each generator.

### Step 4 (optional) - Add LLM solution probes

```bash
python generate_llm_solutions_qiskit_he.py \
  --root ./Framework_Qiskit_Human_Eval/full \
  --scoped \
  --model deepseekv32 \
  --label-oracle
```

Then evaluate **without** `--human-only` so oracle-labeled LLM solutions enter the cohort.

---

## Outputs

```text
Framework_Qiskit_Human_Eval/full/evaluation_results/
  .../test_quality_results_<timestamp>.json
  .../test_quality_report_<timestamp>.md
```

If `|S_w| = 0` for a task, BDS/TQS/CQ are **n/a**.
Metric definitions: [root README](../README.md#what-qtestbench-does).

---

## Default timeouts

| Setting | Value |
|---------|-------|
| Pytest whole file | 240 s |
| Pytest per test | 120 s |
| Oracle labeling | 120 s |

---

## Troubleshooting

| Issue | What to try |
|-------|-------------|
| Missing scope file | Ensure `evaluation_scope_tasks.txt` exists under `full/` |
| Averaging looks wrong | Use `--scoped`; do not evaluate the full corpus unless all tasks have tests |
| API failures | Check `.env` and OpenRouter key / quotas |
| Long runtimes | Start with one model and `--scoped` |

---

## Key scripts

| Script | Role |
|--------|------|
| `prepare_qiskit_human_eval.py` | Build task folders from the dataset JSON |
| `generate_tests_qiskit_he.py` | Stage 1: LLM writes pytest suites |
| `evaluate_qiskit_he.py` | Stage 2: **run tests** and score vs oracle |
| `oracle_qiskit_he.py` | Official checker labeling helper |
| `config.py` | Models, paths, defaults |
