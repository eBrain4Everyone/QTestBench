# QHack Framework Bundle (PennyLane)

How to **generate** and **run** QTestBench unit tests on eight PennyLane QHack challenges.

Parent overview: [root README](../README.md).

---

## Goals of this folder

1. Ask an LLM to write pytest suites (`syntactic`, `semantic`, `behavioral`).
2. **Run those tests** against candidate solutions with pytest.
3. Compare test verdicts to the **official challenge checker** (oracle) and compute ES/CS/BDS/TQS.

Behavioral tests call the candidate local `run()` / `check()` helpers. That is **not** the Stage-2 oracle.

---

## Setup

```bash
cd QHack_Framework_Bundle
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

## How to run the tests (end-to-end)

### Step 1 - Generate pytest modules

```bash
# Recommended first run (one challenge)
python generate_tests.py --model claudeopus46 --only chalet_random_gate
```

Useful variants:

```bash
# All 8 challenges, one model
python generate_tests.py --model claudeopus46

# Multiple models
python generate_tests.py --models claudeopus46 deepseekv32 gemini3pro gpt54 qwen3

# Progress / resume helpers
python generate_tests.py --status
python generate_tests.py --reset --model claudeopus46
```

Generated files:

```text
Framework_Eight_Challenges/generated_tests/<challenge>/<model>/
  test_syntactic.py
  test_semantic.py
  test_behavioral.py
```

### Step 2 - Run and score the generated tests

This is the main command to **run the tests** for QHack:

```bash
# Evaluate the suites for one test-generator model
python evaluate_solutions.py --test-gen-model claudeopus46

# Restrict to one challenge
python evaluate_solutions.py --test-gen-model claudeopus46 --only chalet_random_gate
```

What this does:

1. Loads generated pytest files.
2. Injects each candidate solution at runtime.
3. Runs pytest on the suite.
4. Labels probes with the official checker.
5. Writes ES/CS/BDS/TQS reports.

Outputs:

```text
Framework_Eight_Challenges/evaluation_results/
  .../
    test_quality_results_<timestamp>.json
    test_quality_report_<timestamp>.md
```

### Step 3 - Interpret results

Open the Markdown report for a readable table, or the JSON for exact numbers.
Metric definitions: [root README](../README.md#what-qtestbench-does).

See also:

```bash
python evaluate_solutions.py --help
```

---

## Default timeouts

| Setting | Value |
|---------|-------|
| Pytest whole file | 180 s |
| Pytest per test | 60 s |
| Oracle labeling | 90 s |

---

## Troubleshooting

| Issue | What to try |
|-------|-------------|
| Missing API key | Ensure `.env` exists and `OPENROUTER_API_KEY` is set |
| Import / PennyLane errors | Reinstall with `pip install -r requirements.txt` inside the venv |
| Empty generated tests | Re-run generation with `--reset` for that model |
| Slow runs | Start with `--only <challenge>` |

---

## Key scripts

| Script | Role |
|--------|------|
| `generate_tests.py` | Stage 1: LLM writes pytest suites |
| `evaluate_solutions.py` | Stage 2: **run tests** and score vs oracle |
| `config.py` | Models, paths, defaults |
