# QHack 8-Challenge — Test Quality Evaluation Report

**Validation configuration:** Config 2 — Human + LLM labeled cohort
*Human baseline plus oracle-labeled LLM-generated solutions.*


**Generated:** 2026-05-25T10:41:50.826282
**Test-generation model:** `gpt54`
**Challenges evaluated:** 8
**Config key:** `2`
**LLM solution probes:** gemini, gpt4.1, llama-4, qwen3

---

## Score Definitions

Core correctness metrics (each in **[0.0 – 1.0]** except where noted):

| Score | Full name | Meaning | Ideal |
|-------|-----------|---------|-------|
| **ES** | Executability Score | Test runs without crashing on the human baseline | 1.0 |
| **CS** | Correctness Score | Fraction of oracle-*correct* solutions accepted | 1.0 |
| **BDS** | Bug-Detection Score | Fraction of oracle-*wrong* solutions rejected | 1.0 |
| **TQS** | Test Quality Score | ES × CS × BDS (full eval); ES × CS (human-only) | 1.0 |
| **C_in** | Input coverage | Official inputs exercised in *LLM-written* test code (injected ``TEST_CASES`` block stripped); **1.0** if ``for ... in TEST_CASES`` | 1.0 |
| **Cov_lit** | Literal coverage (diagnostic) | Same literal check on the *full* file — often ~1.0 because inputs appear in the injected list | — |
| **CQ** | Composite | √(TQS × C_in) — balances discrimination and input exercise | 1.0 |
| **Div** | Diversity | √(C_in × breadth); breadth = min(1, #``test_*`` / 3) | 1.0 |

> **Human-only mode:** BDS is not defined; **TQS = ES × CS**.

---

## Solution Correctness (oracle labels)

| Challenge | Total LLM | Correct | Wrong | Unknown |
|-----------|----------:|-------:|------:|--------:|
| chalet_random_gate | 8 | 5 | 3 | 0 |
| coffee_conundrum | 8 | 1 | 4 | 3 |
| contextuality_dunes | 8 | 3 | 4 | 1 |
| mach_zender_cabin | 8 | 3 | 4 | 1 |
| QSP_swamp | 8 | 6 | 1 | 1 |
| rainy_days_retreat | 8 | 4 | 2 | 2 |
| travelling_eigentracks | 8 | 0 | 7 | 1 |
| triple_H_hotel | 8 | 3 | 4 | 1 |

---

## Overall Scores by Challenge

| Challenge | ES | CS | BDS | TQS | C_in | CQ | Div | Human baseline |
|-----------|-----|-----|-----|-----|-----|-----|-----|---------------|
| **chalet_random_gate** | 1.00 █████ | 1.00 █████ | 0.67 ███░░ | **0.67** ███░░ | 0.67 ███░░ | 0.67 ███░░ | 0.67 ███░░ | Solution1 |
| **coffee_conundrum** | 1.00 █████ | 0.33 ██░░░ | 0.67 ███░░ | **0.00** ░░░░░ | 1.00 █████ | 0.00 ░░░░░ | 1.00 █████ | Solution1 |
| **contextuality_dunes** | 1.00 █████ | 1.00 █████ | 0.67 ███░░ | **0.67** ███░░ | 0.67 ███░░ | 0.67 ███░░ | 0.67 ███░░ | Solution1 |
| **mach_zender_cabin** | 1.00 █████ | 1.00 █████ | 0.67 ███░░ | **0.67** ███░░ | 0.67 ███░░ | 0.67 ███░░ | 0.67 ███░░ | Solution1 |
| **QSP_swamp** | 1.00 █████ | 1.00 █████ | 0.67 ███░░ | **0.67** ███░░ | 0.67 ███░░ | 0.67 ███░░ | 0.67 ███░░ | Solution1 |
| **rainy_days_retreat** | 1.00 █████ | 0.40 ██░░░ | 1.00 █████ | **0.40** ██░░░ | 0.67 ███░░ | 0.48 ██░░░ | 0.67 ███░░ | Solution1 |
| **travelling_eigentracks** | 1.00 █████ | 1.00 █████ | 0.67 ███░░ | **0.67** ███░░ | 0.67 ███░░ | 0.67 ███░░ | 0.67 ███░░ | Solution3 |
| **triple_H_hotel** | 1.00 █████ | 1.00 █████ | 0.67 ███░░ | **0.67** ███░░ | 0.67 ███░░ | 0.67 ███░░ | 0.67 ███░░ | Solution3 |
| **AVERAGE** | **1.00** | **0.84** | **0.71** | **0.55** | **0.71** | **0.56** | **0.71** | — |

---

## Per-Challenge Detail

### chalet_random_gate

| Test Type | ES | CS | BDS | TQS | C_in | CQ | Div | pool | wrong | err |
|-----------|-----|-----|-----|-----|-----|-----|-----|------|-------|-----|
| syntactic | 1.00 | 1.00 | 0.00 | **0.00** | 0.00 | 0.00 | 0.00 | 6/6 | 0/3 | — |
| semantic | 1.00 | 1.00 | 1.00 | **1.00** | 1.00 | 1.00 | 1.00 | 6/6 | 3/3 | — |
| behavioral | 1.00 | 1.00 | 1.00 | **1.00** | 1.00 | 1.00 | 1.00 | 6/6 | 3/3 | — |

### coffee_conundrum

| Test Type | ES | CS | BDS | TQS | C_in | CQ | Div | pool | wrong | err |
|-----------|-----|-----|-----|-----|-----|-----|-----|------|-------|-----|
| syntactic | 1.00 | 1.00 | 0.00 | **0.00** | 1.00 | 0.00 | 1.00 | 2/2 | 0/4 | — |
| semantic | 1.00 | 0.00 | 1.00 | **0.00** | 1.00 | 0.00 | 1.00 | 0/2 | 4/4 | — |
| behavioral | 1.00 | 0.00 | 1.00 | **0.00** | 1.00 | 0.00 | 1.00 | 0/2 | 4/4 | — |

### contextuality_dunes

| Test Type | ES | CS | BDS | TQS | C_in | CQ | Div | pool | wrong | err |
|-----------|-----|-----|-----|-----|-----|-----|-----|------|-------|-----|
| syntactic | 1.00 | 1.00 | 0.00 | **0.00** | 0.00 | 0.00 | 0.00 | 4/4 | 0/4 | — |
| semantic | 1.00 | 1.00 | 1.00 | **1.00** | 1.00 | 1.00 | 1.00 | 4/4 | 4/4 | — |
| behavioral | 1.00 | 1.00 | 1.00 | **1.00** | 1.00 | 1.00 | 1.00 | 4/4 | 4/4 | — |

### mach_zender_cabin

| Test Type | ES | CS | BDS | TQS | C_in | CQ | Div | pool | wrong | err |
|-----------|-----|-----|-----|-----|-----|-----|-----|------|-------|-----|
| syntactic | 1.00 | 1.00 | 0.00 | **0.00** | 0.00 | 0.00 | 0.00 | 4/4 | 0/4 | — |
| semantic | 1.00 | 1.00 | 1.00 | **1.00** | 1.00 | 1.00 | 1.00 | 4/4 | 4/4 | — |
| behavioral | 1.00 | 1.00 | 1.00 | **1.00** | 1.00 | 1.00 | 1.00 | 4/4 | 4/4 | — |

### QSP_swamp

| Test Type | ES | CS | BDS | TQS | C_in | CQ | Div | pool | wrong | err |
|-----------|-----|-----|-----|-----|-----|-----|-----|------|-------|-----|
| syntactic | 1.00 | 1.00 | 0.00 | **0.00** | 0.00 | 0.00 | 0.00 | 7/7 | 0/1 | — |
| semantic | 1.00 | 1.00 | 1.00 | **1.00** | 1.00 | 1.00 | 1.00 | 7/7 | 1/1 | — |
| behavioral | 1.00 | 1.00 | 1.00 | **1.00** | 1.00 | 1.00 | 1.00 | 7/7 | 1/1 | — |

### rainy_days_retreat

| Test Type | ES | CS | BDS | TQS | C_in | CQ | Div | pool | wrong | err |
|-----------|-----|-----|-----|-----|-----|-----|-----|------|-------|-----|
| syntactic | 1.00 | 0.00 | 1.00 | **0.00** | 0.00 | 0.00 | 0.00 | 0/5 | 2/2 | — |
| semantic | 1.00 | 0.20 | 1.00 | **0.20** | 1.00 | 0.45 | 1.00 | 1/5 | 2/2 | — |
| behavioral | 1.00 | 1.00 | 1.00 | **1.00** | 1.00 | 1.00 | 1.00 | 5/5 | 2/2 | — |

### travelling_eigentracks

| Test Type | ES | CS | BDS | TQS | C_in | CQ | Div | pool | wrong | err |
|-----------|-----|-----|-----|-----|-----|-----|-----|------|-------|-----|
| syntactic | 1.00 | 1.00 | 0.00 | **0.00** | 0.00 | 0.00 | 0.00 | 1/1 | 0/7 | — |
| semantic | 1.00 | 1.00 | 1.00 | **1.00** | 1.00 | 1.00 | 1.00 | 1/1 | 7/7 | — |
| behavioral | 1.00 | 1.00 | 1.00 | **1.00** | 1.00 | 1.00 | 1.00 | 1/1 | 7/7 | — |

### triple_H_hotel

| Test Type | ES | CS | BDS | TQS | C_in | CQ | Div | pool | wrong | err |
|-----------|-----|-----|-----|-----|-----|-----|-----|------|-------|-----|
| syntactic | 1.00 | 1.00 | 0.00 | **0.00** | 0.00 | 0.00 | 0.00 | 4/4 | 0/4 | — |
| semantic | 1.00 | 1.00 | 1.00 | **1.00** | 1.00 | 1.00 | 1.00 | 4/4 | 4/4 | — |
| behavioral | 1.00 | 1.00 | 1.00 | **1.00** | 1.00 | 1.00 | 1.00 | 4/4 | 4/4 | — |

---

## LLM Solution Results (per challenge)

### chalet_random_gate

| Test Type | gemini/generated_non_rag_1 | gemini/generated_rag_1 | gpt4.1/generated_non_rag_1 | gpt4.1/generated_rag_1 | llama-4/generated_non_rag_1 | llama-4/generated_rag_1 | qwen3/generated_non_rag_1 | qwen3/generated_rag_1 |
|-----------|---|---|---|---|---|---|---|---|
| syntactic | ✓PASS | ⚠PASS | ✓PASS | ✓PASS | ⚠PASS | ⚠PASS | ✓PASS | ✓PASS |
| semantic | ✓PASS | REJECT | ✓PASS | ✓PASS | REJECT | REJECT | ✓PASS | ✓PASS |
| behavioral | ✓PASS | REJECT | ✓PASS | ✓PASS | REJECT | REJECT | ✓PASS | ✓PASS |

### coffee_conundrum

| Test Type | gemini/generated_non_rag_1 | gemini/generated_rag_1 | gpt4.1/generated_non_rag_1 | gpt4.1/generated_rag_1 | llama-4/generated_non_rag_1 | llama-4/generated_rag_1 | qwen3/generated_non_rag_1 | qwen3/generated_rag_1 |
|-----------|---|---|---|---|---|---|---|---|
| syntactic | ⚠PASS | ✗FAIL | ✓PASS | ✗FAIL | ⚠PASS | ⚠PASS | ⚠PASS | ✗FAIL |
| semantic | REJECT | ✗FAIL | ✗FAIL | ✗FAIL | REJECT | REJECT | REJECT | ✗FAIL |
| behavioral | REJECT | ✗FAIL | ✗FAIL | ✗FAIL | REJECT | REJECT | REJECT | ✗FAIL |

### contextuality_dunes

| Test Type | gemini/generated_non_rag_1 | gemini/generated_rag_1 | gpt4.1/generated_non_rag_1 | gpt4.1/generated_rag_1 | llama-4/generated_non_rag_1 | llama-4/generated_rag_1 | qwen3/generated_non_rag_1 | qwen3/generated_rag_1 |
|-----------|---|---|---|---|---|---|---|---|
| syntactic | ⚠PASS | ⚠PASS | ✓PASS | ✓PASS | ✓PASS | ⚠PASS | ⚠PASS | ✗FAIL |
| semantic | REJECT | REJECT | ✓PASS | ✓PASS | ✓PASS | REJECT | REJECT | ✗FAIL |
| behavioral | REJECT | REJECT | ✓PASS | ✓PASS | ✓PASS | REJECT | REJECT | ✗FAIL |

### mach_zender_cabin

| Test Type | gemini/generated_non_rag_1 | gemini/generated_rag_1 | gpt4.1/generated_non_rag_1 | gpt4.1/generated_rag_1 | llama-4/generated_non_rag_1 | llama-4/generated_rag_1 | qwen3/generated_non_rag_1 | qwen3/generated_rag_1 |
|-----------|---|---|---|---|---|---|---|---|
| syntactic | ⚠PASS | ⚠PASS | ✓PASS | ✓PASS | ⚠PASS | ✓PASS | ⚠PASS | ✗FAIL |
| semantic | REJECT | REJECT | ✓PASS | ✓PASS | REJECT | ✓PASS | REJECT | ✗FAIL |
| behavioral | REJECT | REJECT | ✓PASS | ✓PASS | REJECT | ✓PASS | REJECT | ✗FAIL |

### QSP_swamp

| Test Type | gemini/generated_non_rag_1 | gemini/generated_rag_1 | gpt4.1/generated_non_rag_1 | gpt4.1/generated_rag_1 | llama-4/generated_non_rag_1 | llama-4/generated_rag_1 | qwen3/generated_non_rag_1 | qwen3/generated_rag_1 |
|-----------|---|---|---|---|---|---|---|---|
| syntactic | ✓PASS | ✓PASS | ✓PASS | ✓PASS | ✓PASS | ✓PASS | ⚠PASS | ✗FAIL |
| semantic | ✓PASS | ✓PASS | ✓PASS | ✓PASS | ✓PASS | ✓PASS | REJECT | ✗FAIL |
| behavioral | ✓PASS | ✓PASS | ✓PASS | ✓PASS | ✓PASS | ✓PASS | REJECT | ✗FAIL |

### rainy_days_retreat

| Test Type | gemini/generated_non_rag_1 | gemini/generated_rag_1 | gpt4.1/generated_non_rag_1 | gpt4.1/generated_rag_1 | llama-4/generated_non_rag_1 | llama-4/generated_rag_1 | qwen3/generated_non_rag_1 | qwen3/generated_rag_1 |
|-----------|---|---|---|---|---|---|---|---|
| syntactic | ✗FAIL | ✗FAIL | ✗FAIL | REJECT | ✗FAIL | ✗FAIL | REJECT | ✗FAIL |
| semantic | ✗FAIL | ✗FAIL | ✓PASS | REJECT | ✗FAIL | ✗FAIL | REJECT | ✗FAIL |
| behavioral | ✓PASS | ✓PASS | ✓PASS | REJECT | ✗FAIL | ✓PASS | REJECT | ✗FAIL |

### travelling_eigentracks

| Test Type | gemini/generated_non_rag_1 | gemini/generated_rag_1 | gpt4.1/generated_non_rag_1 | gpt4.1/generated_rag_1 | llama-4/generated_non_rag_1 | llama-4/generated_rag_1 | qwen3/generated_non_rag_1 | qwen3/generated_rag_1 |
|-----------|---|---|---|---|---|---|---|---|
| syntactic | ⚠PASS | ⚠PASS | ⚠PASS | ⚠PASS | ⚠PASS | ✗FAIL | ⚠PASS | ⚠PASS |
| semantic | REJECT | REJECT | REJECT | REJECT | REJECT | ✗FAIL | REJECT | REJECT |
| behavioral | REJECT | REJECT | REJECT | REJECT | REJECT | ✗FAIL | REJECT | REJECT |

### triple_H_hotel

| Test Type | gemini/generated_non_rag_1 | gemini/generated_rag_1 | gpt4.1/generated_non_rag_1 | gpt4.1/generated_rag_1 | llama-4/generated_non_rag_1 | llama-4/generated_rag_1 | qwen3/generated_non_rag_1 | qwen3/generated_rag_1 |
|-----------|---|---|---|---|---|---|---|---|
| syntactic | ⚠PASS | ⚠PASS | ⚠PASS | ✓PASS | ✓PASS | ✓PASS | ⚠PASS | ✗FAIL |
| semantic | REJECT | REJECT | REJECT | ✓PASS | ✓PASS | ✓PASS | REJECT | ✗FAIL |
| behavioral | REJECT | REJECT | REJECT | ✓PASS | ✓PASS | ✓PASS | REJECT | ✗FAIL |
