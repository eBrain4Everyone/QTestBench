# LLM-Generated Unit Tests for QHack Challenges  
**Brief for supervisor meeting — approach, metrics, results, interpretation**

---

## 1. Objective

Evaluate whether **large language models (LLMs)** can produce **pytest suites** for eight quantum-programming (QHack) challenges that:

1. **Run reliably** against reference implementations  
2. **Accept** solutions that are **correct** under an official input/output oracle  
3. **Reject** solutions that are **incorrect** under that oracle  
4. Show **adequate exercise** of official test inputs in the **model-written** test code (a coverage-style proxy)

The work implements a **generation pipeline** (OpenRouter), an **evaluation pipeline** (pytest + oracle labels), and **reported metrics** on five test-generation models, in **human-only** and **full** (human + LLM probes) settings.

---

## 2. Approach

### 2.1 Test generation

- **Input to the LLM:** challenge description, official I/O pairs — **not** the full reference solution (reduces copying the answer into tests).  
- **Post-processing:** the framework **prepends** the exact official `TEST_CASES` list so expected outputs are grounded.  
- **Execution model:** tests load the candidate solution at **runtime** via `INJECTED_SOLUTION_CODE` (set in `conftest.py`), not by embedding solution source in the file.  
- **Output:** three files per challenge — **syntactic**, **semantic**, **behavioural** — stored under  
  `Framework_Eight_Challenges/generated_tests/<challenge>/<test_gen_model>/`.

### 2.2 Evaluation

- **Human baseline:** for each challenge, a human submission is selected (by default: the one that scores best on pytest pass count across the three test files; optionally restricted, e.g. `Solution3`).  
- **Human-only run (`--human-only`):** tests are executed **only** against that human solution. Used to measure **baseline agreement** (do tests accept the reference human implementation?).  
- **Full run:** the same tests are run against the **human** plus **LLM-generated solutions** from configured folders. Each LLM solution is labelled **correct / wrong / unknown** by running it on the official cases in a small oracle harness. Used to measure **generalisation** (other correct solutions pass?) and **discrimination** (wrong solutions fail?).

**Scripts:** `generate_tests.py`, `evaluate_solutions.py` — configuration in `config.py`.  
**Artifacts:** timestamped **JSON** (full numbers) and **Markdown** reports under  
`Framework_Eight_Challenges/evaluation_results/human_only/<model>/` and `.../full/<model>/`.

---

## 3. Metrics (definitions and role)

All scores are in **[0, 1]** unless noted; **1** is ideal.

| Metric | Meaning |
|--------|--------|
| **ES** (Executability) | Tests **run** (pytest completes meaningfully on the human baseline without fatal error). |
| **CS** (Correctness) | Fraction of **oracle-correct** solutions in the pool that the suite **fully passes**. Pool = human only (human-only mode) or human + labelled-correct LLMs (full mode). |
| **BDS** (Bug detection) | Fraction of **oracle-wrong** LLM solutions for which the suite **fails** at least one test. **Only in full evaluation.** |
| **TQS** (Test quality) | **Human-only:** ES × CS. **Full:** ES × CS × BDS — high only if tests run, accept correct code, and reject wrong code. |
| **C_in** (Coverage inputs) | After **removing** the injected `TEST_CASES` block, measures whether **LLM-written** test code **references** official inputs (or uses `for ... in TEST_CASES`, counted as full). Avoids inflated “coverage” from the injected list alone. |
| **Cov_lit** | Same literal idea on the **full** file — **diagnostic** only (often near 1 because of injection). |
| **Div** (Diversity) | Combines **C_in** with breadth (number of `test_*` functions). |
| **CQ** | √(TQS × C_in) — optional composite; report **TQS** and **C_in** separately in discussion. |

**Correctness** in this project = **empirical agreement** with the oracle and probe pool, **not** formal verification.  
**Coverage** = **input-level proxy** in test **source**, **not** line/branch coverage of the solution code.

---

## 4. Experimental setup (this study)

| Item | Setting |
|------|--------|
| Challenges | 8 (QHack framework canonical names) |
| Test-generation models compared | `gemini3pro`, `claudeopus46`, `gpt54`, `deepseekv32`, `qwen3` |
| Full-eval LLM probes | Default set in `config.py`: e.g. `gemini`, `gpt4.1`, `llama-4`, `qwen3` × two variants → **8** solutions per challenge |
| Results cited below | Aggregated **average over eight challenges** (report “AVERAGE” row), runs dated **2026-04-02** |

---

## 5. Results

### 5.1 Human-only evaluation (baseline acceptance)

| Model | ES | CS | TQS (= ES×CS) | C_in | CQ | Div |
|-------|-----|-----|---------------|------|-----|-----|
| gemini3pro | 1.00 | 0.96 | **0.96** | 0.71 | 0.67 | 0.71 |
| claudeopus46 | 1.00 | 0.88 | 0.88 | 0.69 | 0.57 | 0.70 |
| gpt54 | 1.00 | 0.83 | 0.83 | 0.71 | 0.58 | 0.71 |
| deepseekv32 | 0.96 | 0.46 | 0.46 | 0.35 | 0.28 | 0.36 |
| qwen3 | 0.79 | 0.38 | 0.38 | 0.44 | 0.12 | 0.43 |

### 5.2 Full evaluation (human + LLM probes)

| Model | ES | CS | BDS | TQS | C_in | CQ | Div |
|-------|-----|-----|-----|-----|------|-----|-----|
| claudeopus46 | 1.00 | 0.88 | **0.80** | **0.68** | 0.69 | 0.55 | 0.70 |
| gemini3pro | 1.00 | 0.96 | 0.67 | 0.62 | 0.71 | 0.62 | 0.71 |
| gpt54 | 1.00 | 0.84 | 0.71 | 0.55 | 0.71 | 0.56 | 0.71 |
| deepseekv32 | 0.96 | 0.47 | 0.75 | 0.26 | 0.35 | 0.27 | 0.36 |
| qwen3 | 0.79 | 0.38 | 0.50 | 0.08 | 0.44 | 0.08 | 0.43 |

*C_in and Div are properties of generated test **source**; they are unchanged between human-only and full runs for the same generator and challenge set.*

---

## 6. Interpretation (discussion points)

1. **Human-only vs full**  
   - Human-only answers: *“Do our tests accept the chosen human baseline?”*  
   - Full evaluation adds: *“Do other oracle-correct LLM solutions pass, and do oracle-wrong ones fail?”*  
   - **TQS** often **drops** in full mode when **BDS < 1** (some incorrect probes still pass) even if **CS** stays high.

2. **Ranking**  
   - **Strongest human-only TQS:** **gemini3pro** — best alignment with the auto-selected human baseline.  
   - **Strongest full TQS (this snapshot):** **claudeopus46** — driven by higher **BDS** (0.80), i.e. better rejection of wrong probes, despite slightly lower human-only TQS than gemini3pro.  
   - **Weakest overall:** **qwen3** and **deepseekv32** — lower ES/CS and, for qwen3, low BDS in full runs.

3. **Cross-challenge effects**  
   - **coffee_conundrum** (and similarly **rainy_days_retreat** in several runs) shows **low CS across models** — suggests **test–reference or oracle mismatch**, not only “weak generator.” Worth discussing as a **data / test-design** issue.  
   - **Syntactic** tests often have **low C_in** (no literals in stripped body); **semantic/behavioural** often use `TEST_CASES` loops → higher **C_in**. Syntactic tests may still **pass wrong** quantum code; **BDS** is frequently lower on syntactic rows in the detailed JSON.

4. **Coverage metric**  
   - **C_in** is a **deliberate, conservative** proxy for “official inputs exercised in LLM-authored lines.” It does **not** replace classical code coverage; state that clearly if writing up.

---

## 7. Limitations (one slide)

- Scores depend on **which** LLM solutions are probed and **oracle** labelling quality.  
- Human baseline is **automatically selected** unless fixed (`--prefer-human-set`).  
- **C_in** does not measure branch/mutation coverage of implementations.

---

## 8. Where the numbers live

- JSON: `Framework_Eight_Challenges/evaluation_results/human_only/<model>/test_quality_results_*.json`  
- Same under `evaluation_results/full/<model>/`  
- Per-run **pytest excerpts** appear in JSON on failures for debugging.

---

## 9. Cross-framework scalability study (see separate file)

The detailed PennyLane (QHack) vs Qiskit HumanEval comparison, interpretation, and scalability evidence checklist are in `COMPARATIVE_FRAMEWORK_SCALABILITY.md`.

### 9.1 Why this comparison matters

The same evaluation design (ES, CS, BDS, TQS, C_in, CQ + synthetic negatives) has now been run on:

- **PennyLane / QHack** challenge set (`Framework_Eight_Challenges`)  
- **Qiskit HumanEval** challenge set (`Framework_Qiskit_Human_Eval`, scoped 10-task run)

This lets us test whether the framework behavior is consistent when moving across:

- different SDKs (PennyLane vs Qiskit),  
- different task corpora and prompt styles,  
- different solution pools.

### 9.2 Snapshot comparison (mean values from current reports)

| Setting | Best model by TQS | TQS range across models | Key pattern |
|---------|-------------------|-------------------------|-------------|
| QHack full (8 challenges) | `claudeopus46` (~0.68) | ~0.08 to ~0.68 | Higher top-end quality; BDS contributes strongly to ranking. |
| Qiskit HumanEval scoped (10 tasks) | `gemini3pro` (~0.53) | ~0.22 to ~0.53 | Moderate quality overall; bigger instability task-to-task (min TQS=0, max=1). |

### 9.3 What this **does** support (positive evidence)

1. **Metric portability:** ES/CS/BDS/TQS/C_in/CQ can be computed and interpreted in both ecosystems with the same meaning.  
2. **Pipeline portability:** generation/evaluation scripts, runtime injection harness, and report structure transfer across frameworks.  
3. **Model sensitivity is preserved:** stronger vs weaker generators are still separable in both settings, so the framework is informative beyond a single benchmark.

### 9.4 What this does **not yet prove**

This is strong **evidence of transferability**, but not full proof of global scalability yet.  
To claim full scalability, you should still add:

- larger Qiskit coverage (beyond the 10-task scope),  
- repeated runs / seeds for stability intervals,  
- optional per-task calibration checks for oracle strictness.

### 9.5 Recommended wording for supervisors/paper

> The framework demonstrates **cross-framework transferability** from PennyLane QHack to Qiskit HumanEval: the same generation-evaluation protocol and quality metrics are operational and discriminative in both settings.  
> Current results provide **evidence of scalability**, while full validation of scalability requires broader task coverage and repeated-run robustness analysis.

---

## 10. Suggested next experiment to strengthen the claim

Run the same 5-model protocol on a larger Qiskit slice (e.g., 30-50 tasks stratified by difficulty), and report:

- mean ± std for ES/CS/BDS/TQS,  
- per-task failure taxonomy (syntax/runtime/spec-mismatch),  
- correlation of rankings between QHack and Qiskit.

If ranking order and metric behavior remain consistent, your scalability claim becomes substantially stronger.

---



*End of brief.*
