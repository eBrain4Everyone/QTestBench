# SEMANTIC tests — Qiskit HumanEval task task_0001
# Generated: 2026-04-28T11:09:11.064829
# Model: anthropic/claude-opus-4-6 (claudeopus46)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    assert isinstance(result, dict)\n    assert result.keys() == {"00", "11"}\n    assert 0.4 < (result["00"] / sum(result.values())) < 0.6\n'
ENTRY_POINT_NAME = 'run_bell_state_simulator'
# --- Official check block end ---
import pytest

def test_run_bell_state_returns_dict_1():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    result = candidate()

    assert isinstance(result, dict), (
        f"Expected return type dict, got {type(result)}"
    )

    # A Bell state (phi+) should only produce '00' and '11' outcomes
    allowed_keys_variants = [
        {"00", "11"},
        {"0x0", "0x3"},  # hex format possible
    ]
    keys = set(result.keys())

    # Normalize keys: convert int keys to binary strings if needed
    normalized = {}
    for k, v in result.items():
        if isinstance(k, int):
            normalized[format(k, '02b')] = v
        elif isinstance(k, str):
            # Handle possible '0x' prefix or space-separated
            clean = k.replace(" ", "")
            normalized[clean] = v
        else:
            normalized[str(k)] = v

    # Check that only '00' and '11' appear (Bell state phi+)
    for key in normalized:
        assert key in ("00", "11"), (
            f"Unexpected measurement outcome '{key}' for phi+ Bell state. "
            f"All keys: {normalized.keys()}"
        )

    assert len(normalized) > 0, "Counts dictionary should not be empty"


def test_run_bell_state_counts_sum_2():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    result = candidate()

    total_counts = sum(result.values())
    # The total number of shots should be positive and reasonable
    assert total_counts > 0, (
        f"Total counts should be positive, got {total_counts}"
    )

    # All values should be non-negative integers
    for key, val in result.items():
        assert isinstance(val, (int, float)), (
            f"Count for key '{key}' should be numeric, got {type(val)}"
        )
        assert val >= 0, (
            f"Count for key '{key}' should be non-negative, got {val}"
        )


def test_run_bell_state_roughly_equal_distribution_3():
    import builtins as _b
    import numpy as np
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    result = candidate()

    # Normalize keys to binary strings
    normalized = {}
    for k, v in result.items():
        if isinstance(k, int):
            normalized[format(k, '02b')] = v
        elif isinstance(k, str):
            clean = k.replace(" ", "")
            normalized[clean] = v
        else:
            normalized[str(k)] = v

    total = sum(normalized.values())

    # For phi+ Bell state, expect roughly 50/50 split between '00' and '11'
    count_00 = normalized.get("00", 0)
    count_11 = normalized.get("11", 0)

    # These two should account for all counts
    assert count_00 + count_11 == total, (
        f"Expected only '00' and '11' outcomes, but total of those "
        f"({count_00 + count_11}) != total counts ({total}). Keys: {normalized.keys()}"
    )

    # Each outcome should be roughly 50% (within a generous tolerance for stochastic results)
    # With typical 1024 shots, we allow a wide margin
    if total >= 100:
        ratio_00 = count_00 / total
        ratio_11 = count_11 / total
        assert 0.15 < ratio_00 < 0.85, (
            f"Expected '00' ratio ~0.5, got {ratio_00:.4f} "
            f"(count_00={count_00}, total={total})"
        )
        assert 0.15 < ratio_11 < 0.85, (
            f"Expected '11' ratio ~0.5, got {ratio_11:.4f} "
            f"(count_11={count_11}, total={total})"
        )