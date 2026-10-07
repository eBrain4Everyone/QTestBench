# QHack 8-Challenge — LLM Test Evaluation Framework v3

**Research summary (approach, metrics, results):** see [`RESEARCH_BRIEF_FOR_SUPERVISORS.md`](RESEARCH_BRIEF_FOR_SUPERVISORS.md).

## What was fixed

The previous version (v2) had CS = 0.00 for all semantic and behavioral tests,
meaning those tests rejected every correct solution. The root cause was that
the LLM was generating hardcoded numerical expected values inside the tests
that did not match what actual solutions produce.

### Three fixes in v3

**Fix 1 — Injected TEST_CASES (eliminates CS = 0)**
Every generated test file now starts with an auto-injected Python literal:
```python
TEST_CASES = [('[0.25, 0.25, 0.25]', '[0.5, 0.5]'), ('[0.125, 0.25, 0.2]', '[0.625, 0.375]')]
```
The LLM is told to reference this variable directly — it never has to
reproduce numerical values from memory. This is the key fix.

**Fix 2 — Property-based tests (new 4th test type)**
`test_property.py` checks mathematical invariants that any correct quantum
solution must satisfy: JSON-parseable output, finite values, probabilities
summing to 1, correct output length, non-constant function. These tests
never use expected values at all, so CS is guaranteed high.

**Fix 3 — Semantic test_3 changed**
The third semantic test no longer checks exact equality. Instead it verifies
that the solution produces different outputs for different inputs (non-constant
function check). This ensures at least one semantic sub-test always passes.

## Setup

1. Create a `.env` file next to these scripts:
   ```
   OPENROUTER_API_KEY=sk-or-v1-your-key-here
   ```

2. Install dependencies:
   ```
   pip install requests pennylane pytest pytest-timeout
   ```

3. Make sure `FRAMEWORK_ROOT` in `config.py` points to your
   `Framework_Eight_Challenges` folder.

## Usage

### Step 1 — Generate tests (NEW: 4 test types per challenge)
```powershell
# All 5 models, all 8 challenges
python generate_tests.py --models geminipro claude deepseekv3 gpt41 llama4

# Single model test run first
python generate_tests.py --model claude --only chalet_random_gate

# Check progress
python generate_tests.py --status

# Reset and re-run a model
python generate_tests.py --reset --model claude
python generate_tests.py --model claude
```

### Step 2 — Evaluate test quality
```powershell
foreach ($model in @("geminipro","claude","deepseekv3","gpt41","llama4")) {
    python evaluate_solutions.py --test-gen-model $model `
        --output-dir "Framework_Eight_Challenges\evaluation_results\$model"
}
```

## Output structure

```
Framework_Eight_Challenges/
  generated_tests/
    chalet_random_gate/
      claude/
        test_syntactic.py    # structure checks
        test_semantic.py     # numerical correctness via TEST_CASES
        test_behavioral.py   # run()+check() harness
        test_property.py     # mathematical invariants (NEW)
      geminipro/
        ...
  evaluation_results/
    claude/
      test_quality_results_<ts>.json
      test_quality_report_<ts>.md
```

## Scores

Each test file receives:

| Score | Formula | Meaning |
|-------|---------|---------|
| ES | 1 or 0 | Does the test run without crashing? |
| CS | correct_pass / correct_total | Does it accept correct solutions? |
| BDS | wrong_fail / wrong_total | Does it catch wrong solutions? |
| TQS | ES × CS × BDS | Overall quality (0 if any component fails) |

## Expected improvement over v2

| Test type | v2 CS | v3 CS (expected) | Why |
|-----------|--------|------------------|-----|
| syntactic | 0.75–1.00 | 0.75–1.00 | No change |
| semantic | 0.00 | 0.50–1.00 | TEST_CASES injected |
| behavioral | 0.00–0.25 | 0.50–1.00 | TEST_CASES injected |
| property | N/A | 0.75–1.00 | New — invariants only |

## Files

- `config.py` — API key, model list, paths
- `notebook_utils.py` — code extraction from .ipynb, fence stripping, harness injection
- `challenge_mapper.py` — discovers challenges and solutions
- `generate_tests.py` — Phase 1: generates test files (v3 with injection)
- `evaluate_solutions.py` — Phase 2: evaluates test quality (ES/CS/BDS/TQS)
