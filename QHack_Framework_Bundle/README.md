# QHack Framework Bundle (PennyLane)

This directory implements the **QHack / PennyLane** half of QTestBench: LLM generation of quantum unit tests and oracle-grounded evaluation on eight QHack challenges.

For the full project overview, metrics, and citation, see the [repository root README](../README.md).

---

## What this bundle does

1. **Generate tests** (`generate_tests.py`)  
   For each challenge, an LLM produces three pytest modules:
   - **syntactic** — structure / entry points (no circuit execution)
   - **semantic** — execution on official inputs with numerical tolerance
   - **behavioral** — end-to-end `run()` then candidate-local `check()`

2. **Evaluate tests** (`evaluate_solutions.py`)  
   Injects candidate solutions at runtime, labels probes with the official challenge checker, and reports ES, CS, BDS, TQS, C_in, and CQ.

**Behavioral note.** On QHack, behavioral suites call the candidate’s template-local `check()`. That helper is **not** the Stage-2 official oracle used for labeling.

---

## Directory layout

```text
QHack_Framework_Bundle/
├── config.py
├── generate_tests.py
├── evaluate_solutions.py
├── challenge_mapper.py
├── notebook_utils.py
├── requirements.txt
├── .env.example
└── Framework_Eight_Challenges/
    ├── Challenges/                 # challenge materials
    ├── Human_solutions/            # trusted human references
    ├── LLM_generated_solutions/    # optional LLM solution probes
    ├── generated_tests/            # LLM-written pytest suites
    └── evaluation_results/         # JSON + Markdown score reports
```

---

## Setup

```bash
cd QHack_Framework_Bundle
python -m venv venv
venv\Scripts\activate          # Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env           # set OPENROUTER_API_KEY=...
```

Confirm `FRAMEWORK_ROOT` in `config.py` points to `Framework_Eight_Challenges`.

---

## Usage

### Generate tests

```bash
# One model, one challenge (smoke test)
python generate_tests.py --model claudeopus46 --only chalet_random_gate

# One model, all eight challenges
python generate_tests.py --model claudeopus46

# Several models
python generate_tests.py --models claudeopus46 deepseekv32 gemini3pro gpt54 qwen3
```

Useful flags:

| Flag | Purpose |
|------|---------|
| `--status` | Show generation progress |
| `--reset` | Clear checkpoint for a model before regenerating |
| `--only <name>` | Restrict to one challenge folder name |

### Evaluate test quality

```bash
python evaluate_solutions.py --test-gen-model claudeopus46
```

Evaluation writes timestamped JSON and Markdown reports under  
`Framework_Eight_Challenges/evaluation_results/`.

---

## Generated test layout

```text
Framework_Eight_Challenges/generated_tests/
  <challenge>/
    <model>/
      test_syntactic.py
      test_semantic.py
      test_behavioral.py
```

Official `TEST_CASES` are injected into generated files so semantic/behavioral assertions stay grounded in benchmark inputs/outputs. The reference solution is **not** shown in generation prompts.

---

## Metrics (summary)

| Score | Meaning |
|-------|---------|
| ES | Suite executes on the trusted baseline without infrastructure failure |
| CS | Fraction of oracle-correct probes accepted |
| BDS | Fraction of oracle-wrong probes rejected (`n/a` if none) |
| TQS | `ES × CS` (Config A) or `ES × CS × BDS` (Configs B/C when defined) |

Full definitions and Configurations A/B/C are documented in the [root README](../README.md).

---

## Default timeouts

| Setting | Value |
|---------|-------|
| Pytest (whole file) | 180 s |
| Pytest (per test) | 60 s |
| Oracle labeling (per candidate) | 90 s |

---

## Models

Paper generators use OpenRouter keys configured in `config.py`  
(examples: `claudeopus46`, `deepseekv32`, `gemini3pro`, `gpt54`, `qwen3`).

---

## Tips

- Start with `--only <challenge>` and one model before a full run.
- Keep API keys in `.env` only; never commit them.
- Prefer the reports under `evaluation_results/` when comparing to the paper tables.
