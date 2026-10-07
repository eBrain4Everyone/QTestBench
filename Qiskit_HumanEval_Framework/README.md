# Qiskit HumanEval Framework

This directory implements the **Qiskit HumanEval** half of QTestBench: LLM generation of quantum unit tests and oracle-grounded evaluation on Qiskit tasks.

For the full project overview, metrics, and citation, see the [repository root README](../README.md).

---

## What this bundle does

1. **Prepare tasks** (`prepare_qiskit_human_eval.py`)  
   Materializes HumanEval records into runnable task folders (prompt, stub, reference solution, official checker).

2. **Generate tests** (`generate_tests_qiskit_he.py`)  
   For each task, an LLM produces three pytest modules:
   - **syntactic** — load / entry-point checks
   - **semantic** — behavior implied by the task prompt
   - **behavioral** — end-to-end entry-point execution

3. **Evaluate tests** (`evaluate_qiskit_he.py`)  
   Injects candidate solutions at runtime, labels probes with the official `check(candidate)` oracle, and reports ES, CS, BDS, TQS, C_in, and CQ.

Generation prompts use the task prompt/stub only. The canonical solution is **not** shown to the test-generation LLM.

---

## Directory layout

```text
Qiskit_HumanEval_Framework/
├── config.py
├── prepare_qiskit_human_eval.py
├── generate_tests_qiskit_he.py
├── generate_llm_solutions_qiskit_he.py   # optional LLM solution probes
├── evaluate_qiskit_he.py
├── oracle_qiskit_he.py
├── requirements.txt
├── .env.example
├── datasets/                            # HumanEval JSON sources
└── Framework_Qiskit_Human_Eval/
    └── full/
        ├── tasks/
        ├── Human_solutions/canonical/
        ├── generated_tests/
        ├── LLM_generated_solutions/
        ├── evaluation_results/
        └── evaluation_scope_tasks.txt   # fixed 10-task paper scope
```

---

## Setup

```bash
cd Qiskit_HumanEval_Framework
python -m venv venv
venv\Scripts\activate          # Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env           # set OPENROUTER_API_KEY=...
```

---

## Paper protocol (recommended)

Reported Qiskit results in the paper use a **fixed 10-task scope**.  
The task list is:

```text
Framework_Qiskit_Human_Eval/full/evaluation_scope_tasks.txt
```

Do **not** average metrics over the full HumanEval corpus unless you generated tests for every task.

### 1) Materialize tasks

```bash
python prepare_qiskit_human_eval.py --only-variant full
```

Optional oracle smoke test:

```bash
python oracle_qiskit_he.py --root ./Framework_Qiskit_Human_Eval/full --limit 3
```

### 2) Generate tests (scoped)

```bash
python generate_tests_qiskit_he.py \
  --root ./Framework_Qiskit_Human_Eval/full \
  --scoped \
  --models claudeopus46 deepseekv32 gemini3pro gpt54 qwen3
```

### 3) Evaluate (trusted baseline + synthetic wrong mutants)

```bash
python evaluate_qiskit_he.py \
  --root ./Framework_Qiskit_Human_Eval/full \
  --scoped \
  --human-only \
  --use-synthetic-negatives \
  --n-synthetic-negatives 3 \
  --test-gen-model claudeopus46
```

Repeat `--test-gen-model` for each generator. Reports are written under `evaluation_results/`.

### 4) Optional: LLM solution probes (Config B-style pool)

```bash
python generate_llm_solutions_qiskit_he.py \
  --root ./Framework_Qiskit_Human_Eval/full \
  --scoped \
  --model deepseekv32 \
  --label-oracle
```

Then evaluate **without** `--human-only` so oracle-labeled LLM solutions are included in the cohort.

---

## Metrics (summary)

| Score | Meaning |
|-------|---------|
| ES | Suite executes on the trusted baseline without infrastructure failure |
| CS | Fraction of oracle-correct probes accepted |
| BDS | Fraction of oracle-wrong probes rejected (`n/a` if none) |
| TQS | `ES × CS` (Config A) or `ES × CS × BDS` (Configs B/C when defined) |

When `|S_w| = 0` for a task, BDS/TQS/CQ are **n/a**. That is why some Qiskit Config B tables omit a pooled TQS column.

Full definitions: [root README](../README.md).

---

## Default timeouts

| Setting | Value |
|---------|-------|
| Pytest (whole file) | 240 s |
| Pytest (per test) | 120 s |
| Oracle labeling (per candidate) | 120 s |

---

## Models

Paper generators use OpenRouter keys configured in `config.py`  
(examples: `claudeopus46`, `deepseekv32`, `gemini3pro`, `gpt54`, `qwen3`).

---

## Tips

- Always prefer `--scoped` for paper-comparable runs.
- Keep API keys in `.env` only; never commit them.
- Generation is single-pass (no repair loop), matching the paper protocol.
