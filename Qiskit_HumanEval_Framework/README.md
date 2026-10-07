# Qiskit HumanEval Framework

Code for generating and evaluating LLM-written pytest suites on Qiskit HumanEval tasks. See the [root README](../README.md) for the overall QTestBench protocol.

## Pipeline

1. `prepare_qiskit_human_eval.py` materializes dataset records into runnable task folders.
2. `generate_tests_qiskit_he.py` asks an LLM for syntactic, semantic, and behavioral pytest modules.
3. `evaluate_qiskit_he.py` runs those tests against candidate solutions and scores them with the official `check(candidate)` oracle.

Generation prompts include the task prompt/stub only; the canonical solution is withheld.

## Setup

```bash
cd Qiskit_HumanEval_Framework
python -m venv venv
venv\Scripts\activate          # Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env           # OPENROUTER_API_KEY=...
```

## Paper protocol (10-task scope)

Use the fixed list in:

```text
Framework_Qiskit_Human_Eval/full/evaluation_scope_tasks.txt
```

and pass `--scoped` for paper-comparable runs.

```bash
# 1) Materialize tasks once
python prepare_qiskit_human_eval.py --only-variant full

# 2) Generate tests
python generate_tests_qiskit_he.py \
  --root ./Framework_Qiskit_Human_Eval/full \
  --scoped \
  --models claudeopus46

# 3) Run tests and score
python evaluate_qiskit_he.py \
  --root ./Framework_Qiskit_Human_Eval/full \
  --scoped \
  --human-only \
  --use-synthetic-negatives \
  --n-synthetic-negatives 3 \
  --test-gen-model claudeopus46
```

Optional LLM solution probes for a richer Config B-style cohort:

```bash
python generate_llm_solutions_qiskit_he.py \
  --root ./Framework_Qiskit_Human_Eval/full \
  --scoped \
  --model deepseekv32 \
  --label-oracle
```

Then evaluate without `--human-only`.

Reports are written under `Framework_Qiskit_Human_Eval/full/evaluation_results/`. When a task has no oracle-wrong probes (`|S_w| = 0`), BDS/TQS/CQ are `n/a`.

## Defaults

| Setting | Value |
|---------|-------|
| Pytest file timeout | 240 s |
| Pytest per-test timeout | 120 s |
| Oracle timeout | 120 s |

Model routing keys are defined in `config.py`.
