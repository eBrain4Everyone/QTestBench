# QHack 8-Challenge — Test Quality Evaluation Report

**Validation configuration:** Config 3 — Human + synthetic wrong negatives
*Human baseline plus oracle-validated synthetic wrong probes.*


**Generated:** 2026-05-25T14:39:20.667448
**Test-generation model:** `qwen3`
**Challenges evaluated:** 8
**Config key:** `3`
**Wrong probes:** synthetic mutants (oracle-validated)

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
| chalet_random_gate | 1 | 0 | 1 | 0 |
| coffee_conundrum | 1 | 0 | 1 | 0 |
| contextuality_dunes | 1 | 0 | 1 | 0 |
| mach_zender_cabin | 1 | 0 | 1 | 0 |
| QSP_swamp | 1 | 0 | 1 | 0 |
| rainy_days_retreat | 1 | 0 | 1 | 0 |
| travelling_eigentracks | 1 | 0 | 1 | 0 |
| triple_H_hotel | 1 | 0 | 1 | 0 |

---

## Overall Scores by Challenge

| Challenge | ES | CS | BDS | TQS | C_in | CQ | Div | Human baseline |
|-----------|-----|-----|-----|-----|-----|-----|-----|---------------|
| **chalet_random_gate** | 0.67 ███░░ | 0.67 ███░░ | 0.33 ██░░░ | **0.33** ██░░░ | 0.67 ███░░ | 0.33 ██░░░ | 0.67 ███░░ | Solution1 |
| **coffee_conundrum** | 1.00 █████ | 0.33 ██░░░ | 0.67 ███░░ | **0.00** ░░░░░ | 1.00 █████ | 0.00 ░░░░░ | 1.00 █████ | Solution1 |
| **contextuality_dunes** | 0.67 ███░░ | 0.33 ██░░░ | 0.33 ██░░░ | **0.00** ░░░░░ | 0.33 ██░░░ | 0.00 ░░░░░ | 0.27 █░░░░ | Solution1 |
| **mach_zender_cabin** | 0.67 ███░░ | 0.33 ██░░░ | 0.33 ██░░░ | **0.00** ░░░░░ | 0.33 ██░░░ | 0.00 ░░░░░ | 0.27 █░░░░ | Solution1 |
| **QSP_swamp** | 0.67 ███░░ | 0.33 ██░░░ | 0.33 ██░░░ | **0.00** ░░░░░ | 0.17 █░░░░ | 0.00 ░░░░░ | 0.24 █░░░░ | Solution1 |
| **rainy_days_retreat** | 1.00 █████ | 0.00 ░░░░░ | 1.00 █████ | **0.00** ░░░░░ | 0.00 ░░░░░ | 0.00 ░░░░░ | 0.00 ░░░░░ | Solution1 |
| **travelling_eigentracks** | 1.00 █████ | 0.67 ███░░ | 0.67 ███░░ | **0.33** ██░░░ | 0.33 ██░░░ | 0.33 ██░░░ | 0.33 ██░░░ | Solution3 |
| **triple_H_hotel** | 0.67 ███░░ | 0.33 ██░░░ | 0.33 ██░░░ | **0.00** ░░░░░ | 0.67 ███░░ | 0.00 ░░░░░ | 0.67 ███░░ | Solution3 |
| **AVERAGE** | **0.79** | **0.38** | **0.50** | **0.08** | **0.44** | **0.08** | **0.43** | — |

---

## Per-Challenge Detail

### chalet_random_gate

| Test Type | ES | CS | BDS | TQS | C_in | CQ | Div | pool | wrong | err |
|-----------|-----|-----|-----|-----|-----|-----|-----|------|-------|-----|
| syntactic | 1.00 | 1.00 | 0.00 | **0.00** | 0.00 | 0.00 | 0.00 | 1/1 | 0/1 | — |
| semantic | 0.00 | 0.00 | 0.00 | **0.00** | 1.00 | 0.00 | 1.00 | 0/0 | 0/0 | `SYNTAX_ERROR` |
| behavioral | 1.00 | 1.00 | 1.00 | **1.00** | 1.00 | 1.00 | 1.00 | 1/1 | 1/1 | — |

### coffee_conundrum

| Test Type | ES | CS | BDS | TQS | C_in | CQ | Div | pool | wrong | err |
|-----------|-----|-----|-----|-----|-----|-----|-----|------|-------|-----|
| syntactic | 1.00 | 1.00 | 0.00 | **0.00** | 1.00 | 0.00 | 1.00 | 1/1 | 0/1 | — |
| semantic | 1.00 | 0.00 | 1.00 | **0.00** | 1.00 | 0.00 | 1.00 | 0/1 | 1/1 | — |
| behavioral | 1.00 | 0.00 | 1.00 | **0.00** | 1.00 | 0.00 | 1.00 | 0/1 | 1/1 | — |

### contextuality_dunes

| Test Type | ES | CS | BDS | TQS | C_in | CQ | Div | pool | wrong | err |
|-----------|-----|-----|-----|-----|-----|-----|-----|------|-------|-----|
| syntactic | 1.00 | 1.00 | 0.00 | **0.00** | 0.00 | 0.00 | 0.00 | 1/1 | 0/1 | — |
| semantic | 0.00 | 0.00 | 0.00 | **0.00** | 1.00 | 0.00 | 0.82 | 0/0 | 0/0 | `SYNTAX_ERROR` |
| behavioral | 1.00 | 0.00 | 1.00 | **0.00** | 0.00 | 0.00 | 0.00 | 0/1 | 1/1 | — |

### mach_zender_cabin

| Test Type | ES | CS | BDS | TQS | C_in | CQ | Div | pool | wrong | err |
|-----------|-----|-----|-----|-----|-----|-----|-----|------|-------|-----|
| syntactic | 1.00 | 1.00 | 0.00 | **0.00** | 0.00 | 0.00 | 0.00 | 1/1 | 0/1 | — |
| semantic | 0.00 | 0.00 | 0.00 | **0.00** | 1.00 | 0.00 | 0.82 | 0/0 | 0/0 | `SYNTAX_ERROR` |
| behavioral | 1.00 | 0.00 | 1.00 | **0.00** | 0.00 | 0.00 | 0.00 | 0/1 | 1/1 | — |

### QSP_swamp

| Test Type | ES | CS | BDS | TQS | C_in | CQ | Div | pool | wrong | err |
|-----------|-----|-----|-----|-----|-----|-----|-----|------|-------|-----|
| syntactic | 1.00 | 1.00 | 0.00 | **0.00** | 0.00 | 0.00 | 0.00 | 1/1 | 0/1 | — |
| semantic | 1.00 | 0.00 | 1.00 | **0.00** | 0.00 | 0.00 | 0.00 | 0/1 | 1/1 | — |
| behavioral | 0.00 | 0.00 | 0.00 | **0.00** | 0.50 | 0.00 | 0.71 | 0/0 | 0/0 | `SYNTAX_ERROR` |

### rainy_days_retreat

| Test Type | ES | CS | BDS | TQS | C_in | CQ | Div | pool | wrong | err |
|-----------|-----|-----|-----|-----|-----|-----|-----|------|-------|-----|
| syntactic | 1.00 | 0.00 | 1.00 | **0.00** | 0.00 | 0.00 | 0.00 | 0/1 | 1/1 | — |
| semantic | 1.00 | 0.00 | 1.00 | **0.00** | 0.00 | 0.00 | 0.00 | 0/1 | 1/1 | — |
| behavioral | 1.00 | 0.00 | 1.00 | **0.00** | 0.00 | 0.00 | 0.00 | 0/1 | 1/1 | — |

### travelling_eigentracks

| Test Type | ES | CS | BDS | TQS | C_in | CQ | Div | pool | wrong | err |
|-----------|-----|-----|-----|-----|-----|-----|-----|------|-------|-----|
| syntactic | 1.00 | 1.00 | 0.00 | **0.00** | 0.00 | 0.00 | 0.00 | 1/1 | 0/1 | — |
| semantic | 1.00 | 0.00 | 1.00 | **0.00** | 0.00 | 0.00 | 0.00 | 0/1 | 1/1 | — |
| behavioral | 1.00 | 1.00 | 1.00 | **1.00** | 1.00 | 1.00 | 1.00 | 1/1 | 1/1 | — |

### triple_H_hotel

| Test Type | ES | CS | BDS | TQS | C_in | CQ | Div | pool | wrong | err |
|-----------|-----|-----|-----|-----|-----|-----|-----|------|-------|-----|
| syntactic | 1.00 | 1.00 | 0.00 | **0.00** | 0.00 | 0.00 | 0.00 | 1/1 | 0/1 | — |
| semantic | 0.00 | 0.00 | 0.00 | **0.00** | 1.00 | 0.00 | 1.00 | 0/0 | 0/0 | `SYNTAX_ERROR` |
| behavioral | 1.00 | 0.00 | 1.00 | **0.00** | 1.00 | 0.00 | 1.00 | 0/1 | 1/1 | — |

---

## LLM Solution Results (per challenge)

### chalet_random_gate

| Test Type | synthetic_wrong/mutant_01 |
|-----------|---|
| syntactic | ⚠PASS |
| semantic | CRASH |
| behavioral | REJECT |

### coffee_conundrum

| Test Type | synthetic_wrong/mutant_01 |
|-----------|---|
| syntactic | ⚠PASS |
| semantic | REJECT |
| behavioral | REJECT |

### contextuality_dunes

| Test Type | synthetic_wrong/mutant_01 |
|-----------|---|
| syntactic | ⚠PASS |
| semantic | CRASH |
| behavioral | REJECT |

### mach_zender_cabin

| Test Type | synthetic_wrong/mutant_01 |
|-----------|---|
| syntactic | ⚠PASS |
| semantic | CRASH |
| behavioral | REJECT |

### QSP_swamp

| Test Type | synthetic_wrong/mutant_01 |
|-----------|---|
| syntactic | ⚠PASS |
| semantic | REJECT |
| behavioral | CRASH |

### rainy_days_retreat

| Test Type | synthetic_wrong/mutant_01 |
|-----------|---|
| syntactic | REJECT |
| semantic | REJECT |
| behavioral | REJECT |

### travelling_eigentracks

| Test Type | synthetic_wrong/mutant_01 |
|-----------|---|
| syntactic | ⚠PASS |
| semantic | REJECT |
| behavioral | REJECT |

### triple_H_hotel

| Test Type | synthetic_wrong/mutant_01 |
|-----------|---|
| syntactic | ⚠PASS |
| semantic | CRASH |
| behavioral | REJECT |
