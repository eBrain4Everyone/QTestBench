# QTestBench

**A test framework for evaluating LLM-generated quantum code**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Venue](https://img.shields.io/badge/IEEE%20QAI-2026-b31b1b.svg)](#citation)

This repository contains the official code for the paper:

> **QTestBench: A Test Framework for Evaluating LLM-Generated Quantum Code**  
> IEEE International Conference on Quantum Artificial Intelligence (QAI), 2026

QTestBench measures whether large language models can write **trustworthy unit tests** for quantum programs. Generated pytest suites are scored against **independent benchmark oracles**, never against the tests themselves.

---

## Why QTestBench?

Existing quantum LLM benchmarks mainly ask: *Can the model write a correct solution?*  
QTestBench asks a different question: *Can the model write tests that accept correct solutions and reject incorrect ones?*

The framework supports two SDKs with the **same metrics and protocol**:

| Benchmark | SDK | Directory |
|-----------|-----|-----------|
| QHack (8 challenges) | PennyLane | [`QHack_Framework_Bundle/`](QHack_Framework_Bundle/) |
| Qiskit HumanEval (10-task paper scope) | Qiskit | [`Qiskit_HumanEval_Framework/`](Qiskit_HumanEval_Framework/) |

---

## Pipeline at a glance

```text
Inputs                         Stage 1                         Stage 2
-------                        --------                        --------
Task description      ->  Generate pytest modules     ->  Build solution cohort
Official test cases       (syntactic / semantic /         Label with official oracle
Official checker            behavioral; single pass)      Execute tests (runtime injection)
                                                          Report ES, CS, BDS, TQS, C_in, CQ
                                                          under Configurations A / B / C
```

**Stage 1 — Test generation**  
One LLM call per test type (temperature 0.8, no repair loop).

**Stage 2 — Validation and scoring**  
Candidate solutions are injected at runtime. The official checker labels each probe as correct, wrong, or unknown. Metrics are aggregated by configuration.

---

## Metrics

| Metric | Meaning |
|--------|---------|
| **ES** | Executability: suite runs without infrastructure failure on the trusted baseline |
| **CS** | Correctness acceptance: fraction of oracle-correct probes accepted |
| **BDS** | Bug detection: fraction of oracle-wrong probes rejected (only when wrong probes exist) |
| **TQS** | Test quality: `ES × CS` (Config A) or `ES × CS × BDS` (Configs B/C when defined) |
| **C_in** | Checker-input coverage in the generated test body |
| **CQ** | Composite quality: `sqrt(TQS × C_in)` when TQS is defined |

If a cohort has no oracle-wrong probes (`|S_w| = 0`), **BDS, TQS, and CQ are reported as n/a** (not zero).

---

## Validation configurations

| Config | Probe cohort | Role |
|--------|--------------|------|
| **A** | Trusted correct reference only | Baseline executability and acceptance |
| **B** | Reference + oracle-labeled LLM solutions | Discrimination on naturally occurring faults |
| **C** | Reference + oracle-verified synthetic mutants | Calibrated bug detection when natural wrong probes are scarce |

---

## Important design notes

1. **Oracle independence.** Generated tests are never ground truth. Only the official checker labels probes.
2. **Behavioral tests (QHack).** These call the candidate’s local `run()` / `check()` helpers. That is **not** the Stage-2 oracle.
3. **Prompt guidance.** Mentions of edge cases or fixed seeds in prompts are soft guidance for stochastic tasks, not hard scoring requirements.
4. **Qiskit paper scope.** Reported Qiskit results use a fixed 10-task list in `evaluation_scope_tasks.txt`. Do not average over the full corpus unless tests exist for every task.

---

## Repository structure

```text
QTestBench/
├── README.md                          # this file
├── LICENSE
├── QHack_Framework_Bundle/            # PennyLane / QHack pipeline
│   ├── README.md                      # setup and commands
│   ├── requirements.txt
│   ├── .env.example
│   ├── generate_tests.py
│   ├── evaluate_solutions.py
│   └── Framework_Eight_Challenges/
└── Qiskit_HumanEval_Framework/        # Qiskit HumanEval pipeline
    ├── README.md                      # setup and commands
    ├── requirements.txt
    ├── .env.example
    ├── prepare_qiskit_human_eval.py
    ├── generate_tests_qiskit_he.py
    ├── evaluate_qiskit_he.py
    └── Framework_Qiskit_Human_Eval/
```

---

## Quick start

### 1. Clone

```bash
git clone https://github.com/eBrain4Everyone/QTestBench.git
cd QTestBench
```

### 2. Install one environment per bundle

```bash
# QHack / PennyLane
cd QHack_Framework_Bundle
python -m venv venv
venv\Scripts\activate          # Linux/macOS: source venv/bin/activate
pip install -r requirements.txt

# Qiskit HumanEval (new terminal)
cd Qiskit_HumanEval_Framework
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. API key (OpenRouter)

```bash
cp QHack_Framework_Bundle/.env.example QHack_Framework_Bundle/.env
cp Qiskit_HumanEval_Framework/.env.example Qiskit_HumanEval_Framework/.env
```

Edit each `.env` and set:

```text
OPENROUTER_API_KEY=sk-or-v1-...
```

Never commit `.env` files.

---

## Reproduce the paper experiments

### QHack (PennyLane)

```bash
cd QHack_Framework_Bundle
python generate_tests.py --model claudeopus46 --only chalet_random_gate
python evaluate_solutions.py --test-gen-model claudeopus46
```

Full options: [`QHack_Framework_Bundle/README.md`](QHack_Framework_Bundle/README.md).

### Qiskit HumanEval (fixed 10-task scope)

```bash
cd Qiskit_HumanEval_Framework
python prepare_qiskit_human_eval.py --only-variant full
python generate_tests_qiskit_he.py --root ./Framework_Qiskit_Human_Eval/full --scoped --models claudeopus46
python evaluate_qiskit_he.py --root ./Framework_Qiskit_Human_Eval/full --scoped --human-only --use-synthetic-negatives --n-synthetic-negatives 3 --test-gen-model claudeopus46
```

Full options: [`Qiskit_HumanEval_Framework/README.md`](Qiskit_HumanEval_Framework/README.md).

---

## Default timeouts

| Setting | QHack | Qiskit HumanEval |
|---------|-------|------------------|
| Pytest (whole file) | 180 s | 240 s |
| Pytest (per test) | 60 s | 120 s |
| Oracle labeling (per candidate) | 90 s | 120 s |

---

## Models

Paper test generators (via OpenRouter): Claude Opus 4.6, DeepSeek V3.2, Gemini 3 Pro, GPT-5.4, and Qwen3-Coder.  
Model routing keys are defined in each bundle’s `config.py`.

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

This work was conducted at the **eBrain Lab**, New York University Abu Dhabi (NYUAD), affiliated with the Center for Cyber Security (CCS) and the Center for Quantum and Topological Systems (CQTS).

We thank the maintainers of the PennyLane QHack challenge materials and the Qiskit HumanEval benchmark for releasing the task resources used in this evaluation.
