# SEMANTIC tests — Qiskit HumanEval task task_0001
# Generated: 2026-04-28T12:27:18.777294
# Model: openai/gpt-5.4 (gpt54)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    assert isinstance(result, dict)\n    assert result.keys() == {"00", "11"}\n    assert 0.4 < (result["00"] / sum(result.values())) < 0.6\n'
ENTRY_POINT_NAME = 'run_bell_state_simulator'
# --- Official check block end ---
def test_bell_counts_supported_keys_1():
    import builtins as _b
    import numpy as np

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    counts = candidate()

    assert isinstance(counts, dict), "The function must return a counts dictionary."
    assert len(counts) > 0, "The returned counts dictionary must not be empty."

    allowed_keys = {"00", "11", 0, 3}
    bad_keys = [k for k in counts.keys() if k not in allowed_keys]
    assert not bad_keys, f"Bell-state counts should only contain outcomes 00 and 11; found unexpected keys: {bad_keys}"

    values = list(counts.values())
    assert all(isinstance(v, (int, float, np.integer, np.floating)) for v in values), "All count values must be numeric."
    assert all(v >= 0 for v in values), "All count values must be non-negative."


def test_bell_distribution_balanced_2():
    import builtins as _b
    import numpy as np

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    counts = candidate()
    assert isinstance(counts, dict), "The function must return a dictionary of counts."

    c00 = counts.get("00", counts.get(0, 0))
    c11 = counts.get("11", counts.get(3, 0))
    total = sum(counts.values())

    assert total > 0, "Total counts must be positive."
    p00 = c00 / total
    p11 = c11 / total

    assert np.allclose(p00 + p11, 1.0, atol=1e-4, rtol=1e-5), "Only 00 and 11 should have nonzero probability for a phi-plus Bell state."
    assert np.allclose(p00, 0.5, atol=0.2, rtol=1e-5), f"Outcome 00 should occur with about 50% probability; got {p00}."
    assert np.allclose(p11, 0.5, atol=0.2, rtol=1e-5), f"Outcome 11 should occur with about 50% probability; got {p11}."


def test_bell_state_correlations_3():
    import builtins as _b
    import numpy as np

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    counts = candidate()
    assert isinstance(counts, dict), "The function must return a dictionary."

    c00 = counts.get("00", counts.get(0, 0))
    c01 = counts.get("01", counts.get(1, 0))
    c10 = counts.get("10", counts.get(2, 0))
    c11 = counts.get("11", counts.get(3, 0))
    total = c00 + c01 + c10 + c11

    assert total > 0, "The counts dictionary must represent at least one shot."
    parity_correlation = (c00 + c11 - c01 - c10) / total

    assert np.allclose(parity_correlation, 1.0, atol=0.2, rtol=1e-5), (
        f"A phi-plus Bell state should show near-perfect even-parity correlation; got correlation {parity_correlation}."
    )
    assert c01 + c10 == 0 or np.allclose((c01 + c10) / total, 0.0, atol=0.2, rtol=1e-5), (
        "Odd-parity outcomes 01 and 10 should be absent or negligible for a phi-plus Bell state."
    )