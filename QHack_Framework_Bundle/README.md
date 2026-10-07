# QHack Framework Bundle (PennyLane)

Code for generating and evaluating LLM-written pytest suites on eight PennyLane QHack challenges. See the [root README](../README.md) for the overall QTestBench protocol.

## Pipeline

1. `generate_tests.py` asks an LLM for three pytest modules per challenge: syntactic, semantic, and behavioral.
2. `evaluate_solutions.py` injects candidate solutions, runs the generated tests with pytest, labels probes with the official checker, and reports ES/CS/BDS/TQS.

Behavioral suites call the candidate's local `run()` / `check()` helpers. Those helpers are not the Stage-2 oracle.

## Setup

```bash
cd QHack_Framework_Bundle
python -m venv venv
venv\Scripts\activate          # Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env           # OPENROUTER_API_KEY=...
```

## Run generation and evaluation

```bash
# Generate tests for one challenge (recommended first run)
python generate_tests.py --model claudeopus46 --only chalet_random_gate

# Run the generated tests and compute scores
python evaluate_solutions.py --test-gen-model claudeopus46 --only chalet_random_gate
```

Additional examples:

```bash
python generate_tests.py --model claudeopus46
python generate_tests.py --models claudeopus46 deepseekv32 gemini3pro gpt54 qwen3
python generate_tests.py --status
python evaluate_solutions.py --test-gen-model claudeopus46
python evaluate_solutions.py --help
```

Generated tests are stored under:

```text
Framework_Eight_Challenges/generated_tests/<challenge>/<model>/
  test_syntactic.py
  test_semantic.py
  test_behavioral.py
```

Evaluation writes JSON and Markdown reports under `Framework_Eight_Challenges/evaluation_results/`.

## Defaults

| Setting | Value |
|---------|-------|
| Pytest file timeout | 180 s |
| Pytest per-test timeout | 60 s |
| Oracle timeout | 90 s |

Model routing keys are defined in `config.py`.
