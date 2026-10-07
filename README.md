# QTestBench: A Test Framework for Evaluating LLM-Generated Quantum Code

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

This repository contains the code for the paper **"QTestBench: A Test Framework for Evaluating LLM-Generated Quantum Code,"** accepted at the **IEEE International Conference on Quantum Artificial Intelligence (QAI 2026)**.

QTestBench evaluates LLM-generated quantum unit-test suites against independent benchmark checkers. The generated tests are never used as ground truth. The same protocol and metrics are applied to:

| Benchmark | SDK | Directory |
|-----------|-----|-----------|
| QHack (8 challenges) | PennyLane | [`QHack_Framework_Bundle/`](QHack_Framework_Bundle/) |
| Qiskit HumanEval (10-task paper scope) | Qiskit | [`Qiskit_HumanEval_Framework/`](Qiskit_HumanEval_Framework/) |

Each subdirectory README explains how to install dependencies and how to run generation and evaluation for that benchmark.

---

## Overview

QTestBench has two stages.

**Stage 1 — Test generation.** For each task, an LLM produces three pytest modules (syntactic, semantic, and behavioral) in a single pass (temperature 0.8, no repair loop).

**Stage 2 — Validation and scoring.** Candidate solutions are injected at runtime. An official benchmark checker labels each probe correct, wrong, or unknown. Suites are scored with ES, CS, BDS, TQS, C_in, and CQ under Configurations A, B, and C.

| Metric | Definition |
|--------|------------|
| ES | 1 if the suite runs on the trusted baseline without infrastructure failure |
| CS | Fraction of oracle-correct probes accepted by the suite |
| BDS | Fraction of oracle-wrong probes rejected (`n/a` when no wrong probes exist) |
| TQS | `ES × CS` in Config A; `ES × CS × BDS` in Configs B/C when BDS is defined |
| C_in | Fraction of official checker input literals present in the generated test body |
| CQ | `√(TQS × C_in)` when TQS is defined |

| Config | Cohort | Role |
|--------|--------|------|
| A | Trusted reference only | Executability and acceptance |
| B | Reference + oracle-labeled LLM solutions | Discrimination on natural faults |
| C | Reference + oracle-verified synthetic mutants | Bug detection when natural wrong probes are scarce |

On QHack, behavioral tests call the candidate's local `run()` / `check()` helpers; those helpers are not the Stage-2 oracle. Mentions of edge cases or fixed seeds in prompts are guidance only and are not enforced by scoring. When `|S_w| = 0`, BDS, TQS, and CQ are reported as `n/a`.

---

## Setup

```bash
git clone https://github.com/eBrain4Everyone/QTestBench.git
cd QTestBench
```

Use a separate virtual environment for each bundle.

**QHack / PennyLane**

```bash
cd QHack_Framework_Bundle
python -m venv venv
venv\Scripts\activate          # Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env           # set OPENROUTER_API_KEY
```

**Qiskit HumanEval**

```bash
cd Qiskit_HumanEval_Framework
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env           # set OPENROUTER_API_KEY
```

An OpenRouter key is required only to generate new tests. Existing generated suites and evaluation reports in the repository can be inspected without a key.

---

## Running the evaluation

### QHack (PennyLane)

```bash
cd QHack_Framework_Bundle

# Stage 1: generate tests (smoke example)
python generate_tests.py --model claudeopus46 --only chalet_random_gate

# Stage 2: run the generated tests and score them
python evaluate_solutions.py --test-gen-model claudeopus46 --only chalet_random_gate
```

Reports are written under `Framework_Eight_Challenges/evaluation_results/`.  
Full options: [`QHack_Framework_Bundle/README.md`](QHack_Framework_Bundle/README.md).

### Qiskit HumanEval (fixed 10-task scope)

Paper results use `Framework_Qiskit_Human_Eval/full/evaluation_scope_tasks.txt`. Prefer `--scoped`.

```bash
cd Qiskit_HumanEval_Framework

python prepare_qiskit_human_eval.py --only-variant full

python generate_tests_qiskit_he.py \
  --root ./Framework_Qiskit_Human_Eval/full \
  --scoped \
  --models claudeopus46

python evaluate_qiskit_he.py \
  --root ./Framework_Qiskit_Human_Eval/full \
  --scoped \
  --human-only \
  --use-synthetic-negatives \
  --n-synthetic-negatives 3 \
  --test-gen-model claudeopus46
```

Full options: [`Qiskit_HumanEval_Framework/README.md`](Qiskit_HumanEval_Framework/README.md).

---

## Outputs and timeouts

| Artifact | QHack | Qiskit |
|----------|-------|--------|
| Generated tests | `Framework_Eight_Challenges/generated_tests/` | `Framework_Qiskit_Human_Eval/full/generated_tests/` |
| Evaluation reports | `Framework_Eight_Challenges/evaluation_results/` | `Framework_Qiskit_Human_Eval/full/evaluation_results/` |

| Setting | QHack | Qiskit |
|---------|-------|--------|
| Pytest (file) | 180 s | 240 s |
| Pytest (per test) | 60 s | 120 s |
| Oracle labeling | 90 s | 120 s |

Paper generators (OpenRouter): Claude Opus 4.6, DeepSeek V3.2, Gemini 3 Pro, GPT-5.4, Qwen3-Coder. Model keys are listed in each bundle's `config.py`.

---

## Citation

```bibtex
@inproceedings{terki2026qtestbench,
  title     = {QTestBench: A Test Framework for Evaluating LLM-Generated Quantum Code},
  author    = {Terki, Meriem and Innan, Nouhaila and Shao, Minghao and Kashif, Muhammad and Marchisio, Alberto and Shafique, Muhammad},
  booktitle = {IEEE International Conference on Quantum Artificial Intelligence (QAI)},
  year      = {2026}
}
```

---

## License

MIT License. See [LICENSE](LICENSE).

---

## Acknowledgements

This work was conducted at the eBrain Lab, New York University Abu Dhabi (NYUAD), affiliated with the Center for Cyber Security (CCS) and the Center for Quantum and Topological Systems (CQTS).

The evaluation uses QHack challenge materials from Xanadu and tasks from the Qiskit HumanEval benchmark.
