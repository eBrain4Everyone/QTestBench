# QHack 8-Challenge — Test Quality Evaluation Report

**Validation configuration:** Config 1 — Human/canonical solutions only
*Reference (canonical) solution only; TQS = ES × CS.*


**Generated:** 2026-05-24T23:02:28.352753
**Test-generation model:** `deepseekv32`
**Challenges evaluated:** 8
**Config key:** `1`

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
| chalet_random_gate | 0 | 0 | 0 | 0 |
| coffee_conundrum | 0 | 0 | 0 | 0 |
| contextuality_dunes | 0 | 0 | 0 | 0 |
| mach_zender_cabin | 0 | 0 | 0 | 0 |
| QSP_swamp | 0 | 0 | 0 | 0 |
| rainy_days_retreat | 0 | 0 | 0 | 0 |
| travelling_eigentracks | 0 | 0 | 0 | 0 |
| triple_H_hotel | 0 | 0 | 0 | 0 |

---

## Overall Scores by Challenge

| Challenge | ES | CS | BDS | TQS | C_in | CQ | Div | Human baseline |
|-----------|-----|-----|-----|-----|-----|-----|-----|---------------|
| **chalet_random_gate** | 0.67 ███░░ | 0.33 ██░░░ | 0.00 ░░░░░ | **0.33** ██░░░ | 0.33 ██░░░ | 0.33 ██░░░ | 0.33 ██░░░ | Solution1 |
| **coffee_conundrum** | 1.00 █████ | 0.67 ███░░ | 0.00 ░░░░░ | **0.67** ███░░ | 0.83 ████░ | 0.57 ███░░ | 0.90 █████ | Solution1 |
| **contextuality_dunes** | 1.00 █████ | 0.67 ███░░ | 0.00 ░░░░░ | **0.67** ███░░ | 0.33 ██░░░ | 0.33 ██░░░ | 0.33 ██░░░ | Solution1 |
| **mach_zender_cabin** | 1.00 █████ | 0.67 ███░░ | 0.00 ░░░░░ | **0.67** ███░░ | 0.33 ██░░░ | 0.33 ██░░░ | 0.33 ██░░░ | Solution1 |
| **QSP_swamp** | 1.00 █████ | 0.33 ██░░░ | 0.00 ░░░░░ | **0.33** ██░░░ | 0.33 ██░░░ | 0.33 ██░░░ | 0.33 ██░░░ | Solution1 |
| **rainy_days_retreat** | 1.00 █████ | 0.00 ░░░░░ | 0.00 ░░░░░ | **0.00** ░░░░░ | 0.33 ██░░░ | 0.00 ░░░░░ | 0.33 ██░░░ | Solution1 |
| **travelling_eigentracks** | 1.00 █████ | 0.67 ███░░ | 0.00 ░░░░░ | **0.67** ███░░ | 0.33 ██░░░ | 0.33 ██░░░ | 0.33 ██░░░ | Solution3 |
| **triple_H_hotel** | 1.00 █████ | 0.00 ░░░░░ | 0.00 ░░░░░ | **0.00** ░░░░░ | 0.00 ░░░░░ | 0.00 ░░░░░ | 0.00 ░░░░░ | Solution1 |
| **AVERAGE** | **0.96** | **0.42** | **0.00** | **0.42** | **0.35** | **0.28** | **0.36** | — |

---

## Per-Challenge Detail

### chalet_random_gate

| Test Type | ES | CS | C_in | CQ | Div | Error |
|-----------|-----|-----|-----|-----|-----|-------|
| syntactic | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | `RUNTIME_ERROR` |
| semantic | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | — |
| behavioral | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | — |

### coffee_conundrum

| Test Type | ES | CS | C_in | CQ | Div | Error |
|-----------|-----|-----|-----|-----|-----|-------|
| syntactic | 1.00 | 1.00 | 0.50 | 0.71 | 0.71 | — |
| semantic | 1.00 | 0.00 | 1.00 | 0.00 | 1.00 | — |
| behavioral | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | — |

### contextuality_dunes

| Test Type | ES | CS | C_in | CQ | Div | Error |
|-----------|-----|-----|-----|-----|-----|-------|
| syntactic | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | — |
| semantic | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | — |
| behavioral | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | — |

### mach_zender_cabin

| Test Type | ES | CS | C_in | CQ | Div | Error |
|-----------|-----|-----|-----|-----|-----|-------|
| syntactic | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | — |
| semantic | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | — |
| behavioral | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | — |

### QSP_swamp

| Test Type | ES | CS | C_in | CQ | Div | Error |
|-----------|-----|-----|-----|-----|-----|-------|
| syntactic | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | — |
| semantic | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | — |
| behavioral | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | — |

### rainy_days_retreat

| Test Type | ES | CS | C_in | CQ | Div | Error |
|-----------|-----|-----|-----|-----|-----|-------|
| syntactic | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | — |
| semantic | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | — |
| behavioral | 1.00 | 0.00 | 1.00 | 0.00 | 1.00 | — |

### travelling_eigentracks

| Test Type | ES | CS | C_in | CQ | Div | Error |
|-----------|-----|-----|-----|-----|-----|-------|
| syntactic | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | — |
| semantic | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | — |
| behavioral | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | — |

### triple_H_hotel

| Test Type | ES | CS | C_in | CQ | Div | Error |
|-----------|-----|-----|-----|-----|-----|-------|
| syntactic | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | — |
| semantic | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | — |
| behavioral | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | — |
