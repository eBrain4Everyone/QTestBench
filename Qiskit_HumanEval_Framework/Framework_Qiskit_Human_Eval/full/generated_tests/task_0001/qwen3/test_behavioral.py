# BEHAVIORAL tests — Qiskit HumanEval task task_0001
# Generated: 2026-04-28T12:39:14.890374
# Model: qwen/qwen3-coder-next (qwen3)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    assert isinstance(result, dict)\n    assert result.keys() == {"00", "11"}\n    assert 0.4 < (result["00"] / sum(result.values())) < 0.6\n'
ENTRY_POINT_NAME = 'run_bell_state_simulator'
# --- Official check block end ---
def test_run_bell_state_simulator_output_structure():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    result = candidate()
    assert isinstance(result, dict), "run_bell_state_simulator must return a dictionary"
    assert set(result.keys()).issubset({'00', '01', '10', '11'}), "Keys must be 2-bit binary strings"
    assert len(result) >= 2, "Bell state should have at least two non-zero measurement outcomes"
    total_counts = sum(result.values())
    assert total_counts > 0, "Total counts must be positive"


def test_run_bell_state_simulator_bell_state_signature():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    result = candidate()
    # For |_+_ = (|00_ + |11_)/_2, we expect ~50% counts for '00' and '11'
    # With small shot counts (e.g., 1024), allow some tolerance
    if '00' in result and '11' in result:
        p_00 = result['00'] / sum(result.values())
        p_11 = result['11'] / sum(result.values())
        assert abs(p_00 - 0.5) < 0.15 and abs(p_11 - 0.5) < 0.15, "Bell state |_+_ should have ~50% '00' and '11' outcomes"
    else:
        # If either key missing, check that the sum of present keys is close to 1.0 and both expected states are present
        raise AssertionError("Missing expected Bell state measurement outcomes '00' and '11'")


def test_run_bell_state_simulator_consistent_with_sampler_api():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    result = candidate()
    # Check that all counts are non-negative integers
    for key, count in result.items():
        assert isinstance(count, int), f"Count for key '{key}' must be an integer"
        assert count >= 0, f"Count for key '{key}' must be non-negative"
    
    # Verify that all counts are non-zero (within statistical fluctuation tolerance) and consistent
    # with a Bell state measurement (no '01' or '10')
    # Allow minimal '01'/'10' counts due to noise, but keep shots low so they should be near-zero
    total = sum(result.values())
    p_01_10 = 0
    if '01' in result:
        p_01_10 += result['01'] / total
    if '10' in result:
        p_01_10 += result['10'] / total
    # For optimized circuit with AerSimulator and Sampler, error rate should be low
    assert p_01_10 < 0.2, f"Unwanted outcomes '01' and '10' should be minimal (<20%); got {p_01_10:.2%}"