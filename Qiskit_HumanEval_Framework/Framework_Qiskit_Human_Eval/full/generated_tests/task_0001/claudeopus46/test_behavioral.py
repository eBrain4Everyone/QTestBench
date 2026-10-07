# BEHAVIORAL tests — Qiskit HumanEval task task_0001
# Generated: 2026-04-28T11:09:32.846856
# Model: anthropic/claude-opus-4-6 (claudeopus46)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    assert isinstance(result, dict)\n    assert result.keys() == {"00", "11"}\n    assert 0.4 < (result["00"] / sum(result.values())) < 0.6\n'
ENTRY_POINT_NAME = 'run_bell_state_simulator'
# --- Official check block end ---
def test_run_bell_state_returns_dict_1():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    result = candidate()

    assert isinstance(result, dict), f"Expected dict, got {type(result)}"
    # Bell state phi+ should only produce '00' and '11' outcomes
    valid_keys = {"00", "11"}
    for key in result:
        # Strip any spaces or leading zeros issues; normalize
        stripped = key.replace(" ", "")
        assert stripped in valid_keys, (
            f"Unexpected measurement outcome '{key}' in counts. "
            f"Phi+ Bell state should only produce '00' or '11'."
        )


def test_run_bell_state_correct_total_counts_2():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    result = candidate()

    assert isinstance(result, dict), f"Expected dict, got {type(result)}"
    total = sum(result.values())
    # Default shots for Sampler is typically 1024 or some positive number
    assert total > 0, f"Total counts should be positive, got {total}"
    # All counts should be non-negative integers
    for key, val in result.items():
        assert isinstance(val, (int, float)), (
            f"Count for '{key}' should be numeric, got {type(val)}"
        )
        assert val >= 0, f"Count for '{key}' should be non-negative, got {val}"


def test_run_bell_state_roughly_equal_distribution_3():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    result = candidate()

    assert isinstance(result, dict), f"Expected dict, got {type(result)}"
    total = sum(result.values())
    assert total > 0, f"Total counts must be positive, got {total}"

    # Normalize keys (strip spaces)
    normalized = {}
    for k, v in result.items():
        nk = k.replace(" ", "")
        normalized[nk] = normalized.get(nk, 0) + v

    # Phi+ Bell state: expect roughly 50/50 split between '00' and '11'
    count_00 = normalized.get("00", 0)
    count_11 = normalized.get("11", 0)

    assert count_00 + count_11 == total, (
        f"All counts should be '00' or '11', but got {normalized}"
    )

    # Each outcome should be at least 20% of total (very loose bound for statistical tolerance)
    ratio_00 = count_00 / total
    ratio_11 = count_11 / total
    assert ratio_00 > 0.2, (
        f"Expected '00' to appear ~50% of time, got {ratio_00:.2%}"
    )
    assert ratio_11 > 0.2, (
        f"Expected '11' to appear ~50% of time, got {ratio_11:.2%}"
    )
    # Also check they are roughly balanced (within 30% tolerance of each other)
    assert abs(ratio_00 - 0.5) < 0.3, (
        f"'00' ratio {ratio_00:.2%} is too far from 50%"
    )
    assert abs(ratio_11 - 0.5) < 0.3, (
        f"'11' ratio {ratio_11:.2%} is too far from 50%"
    )