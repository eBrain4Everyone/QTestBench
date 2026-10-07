# QTestBench

**A test framework for evaluating LLM-generated quantum code**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Venue](https://img.shields.io/badge/IEEE%20QAI-2026-b31b1b.svg)](#citation)

Official code for:

> **QTestBench: A Test Framework for Evaluating LLM-Generated Quantum Code**  
> IEEE International Conference on Quantum Artificial Intelligence (QAI), 2026

QTestBench evaluates whether LLMs can write **trustworthy quantum unit tests**.
Generated pytest suites are scored against **independent benchmark oracles**, never against the tests themselves.

This repository is intended to be **open source** and to accompany the paper. The sections below explain how to install the framework and **how to run the tests / evaluation pipeline**.

---

## Contents

| Path | What it contains |
|------|------------------|
| [`QHack_Framework_Bundle/`](QHack_Framework_Bundle/) | PennyLane QHack pipeline (8 challenges) and how to run it |
| [`Qiskit_HumanEval_Framework/`](Qiskit_HumanEval_Framework/) | Qiskit HumanEval pipeline (10-task paper scope) and how to run it |
| [`LICENSE`](LICENSE) | MIT License |

---

## What QTestBench does

```text
Stage 1: Test generation                 Stage 2: Validation and scoring
-------------------------                 --------------------------------
LLM writes 3 pytest modules               Inject candidate solutions
  - syntactic                             Label probes with official oracle
  - semantic                              Run generated tests (pytest)
  - behavioral                            Score ES / CS / BDS / TQS / C_in / CQ
(single pass, temperature 0.8)            under Configurations A / B / C
```

| Metric | Meaning |
|--------|---------|
| **ES** | Suite runs without infrastructure failure on the trusted baseline |
| **CS** | Fraction of oracle-correct probes accepted |
| **BDS** | Fraction of oracle-wrong probes rejected (`n/a` if none) |
| **TQS** | `ES x CS` (Config A) or `ES x CS x BDS` (Configs B/C when defined) |
| **C_in** | Coverage of official checker inputs in the generated test body |
| **CQ** | `sqrt(TQS x C_in)` when TQS is defined |

| Config | Probe set | Purpose |
|--------|-----------|---------|
| **A** | Trusted correct reference only | Executability and acceptance |
| **B** | + oracle-labeled LLM solutions | Natural bug discrimination |
| **C** | + oracle-verified synthetic mutants | Calibrated bug detection |

**Notes (paper):**

- Generated tests are never ground truth; only the official checker labels probes.
- On QHack, behavioral tests call the candidate local `run()` / `check()` helpers (not the Stage-2 oracle).
- Edge cases / fixed seeds in prompts are soft guidance, not hard scoring rules.
- If `|S_w| = 0`, BDS/TQS/CQ are **n/a** (not 0).

---

## Prerequisites

- Python 3.10+ recommended
- An [OpenRouter](https://openrouter.ai) API key (needed to **generate** new tests)
- Internet access for model calls during generation

You do **not** need an API key only to inspect already-generated tests and reports shipped in the repository.

---

## How to run the tests (quick path)

### 0) Clone

```bash
git clone https://github.com/eBrain4Everyone/QTestBench.git
cd QTestBench
```

### 1) QHack / PennyLane

```bash
cd QHack_Framework_Bundle
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
# source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env and set: OPENROUTER_API_KEY=sk-or-v1-...
```

Generate tests (Stage 1):

```bash
python generate_tests.py --model claudeopus46 --only chalet_random_gate
```

**Run / evaluate those tests** (Stage 2):

```bash
python evaluate_solutions.py --test-gen-model claudeopus46 --only chalet_random_gate
```

Reports appear under `Framework_Eight_Challenges/evaluation_results/`.

Full guide: [`QHack_Framework_Bundle/README.md`](QHack_Framework_Bundle/README.md).

### 2) Qiskit HumanEval (paper 10-task scope)

```bash
cd Qiskit_HumanEval_Framework
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# edit .env and set OPENROUTER_API_KEY
```

```bash
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

Full guide: [`Qiskit_HumanEval_Framework/README.md`](Qiskit_HumanEval_Framework/README.md).

---

## Where outputs are written

| Artifact | QHack | Qiskit |
|----------|-------|--------|
| Generated pytest suites | `Framework_Eight_Challenges/generated_tests/` | `Framework_Qiskit_Human_Eval/full/generated_tests/` |
| Score reports (JSON/MD) | `Framework_Eight_Challenges/evaluation_results/` | `Framework_Qiskit_Human_Eval/full/evaluation_results/` |

Each evaluation run produces machine-readable JSON and a human-readable Markdown report.

---

## Default timeouts

| Setting | QHack | Qiskit |
|---------|-------|--------|
| Pytest (whole file) | 180 s | 240 s |
| Pytest (per test) | 60 s | 120 s |
| Oracle labeling | 90 s | 120 s |

---

## Models used in the paper

Claude Opus 4.6, DeepSeek V3.2, Gemini 3 Pro, GPT-5.4, Qwen3-Coder (via OpenRouter).
Model keys are defined in each bundle `config.py` (examples: `claudeopus46`, `deepseekv32`, `gemini3pro`, `gpt54`, `qwen3`).

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
