# SEMANTIC tests — Qiskit HumanEval task task_0001
# Generated: 2026-04-28T12:39:06.128521
# Model: qwen/qwen3-coder-next (qwen3)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    assert isinstance(result, dict)\n    assert result.keys() == {"00", "11"}\n    assert 0.4 < (result["00"] / sum(result.values())) < 0.6\n'
ENTRY_POINT_NAME = 'run_bell_state_simulator'
# --- Official check block end ---
def test_bell_state_counts():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    result = candidate()
    
    # Check that result is a dictionary
    assert isinstance(result, dict), f"Expected dict, got {type(result)}"
    
    # Check for expected keys: '00' and '11' with high probability for Bell state |_+>
    assert '00' in result, "Missing '00' in result counts"
    assert '11' in result, "Missing '11' in result counts"
    
    # Check that other computational basis states are not present or have negligible counts
    for key in result:
        assert key in ['00', '11'], f"Unexpected key '{key}' in counts dictionary"
    
    # Check that the two expected outcomes have approximately equal probability (within reasonable tolerance)
    total = sum(result.values())
    p00 = result['00'] / total
    p11 = result['11'] / total
    
    assert abs(p00 - 0.5) < 0.1, f"Expected ~50% for |00>, got {p00*100:.2f}%"
    assert abs(p11 - 0.5) < 0.1, f"Expected ~50% for |11>, got {p11*100:.2f}%"
    
    # Check that there are no negative counts
    for count in result.values():
        assert count >= 0, "Counts must be non-negative"


def test_bell_state_circuit_properties():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    # This test indirectly checks correctness by verifying the expected counts
    result = candidate()
    
    # For the Bell state |_+> = (|00_ + |11_)/_2, the measurement outcomes should be perfectly correlated
    # i.e., if first qubit is 0, second is 0; if first is 1, second is 1
    total = sum(result.values())
    
    # Count cases where qubits match vs. don't match
    matching = result.get('00', 0) + result.get('11', 0)
    non_matching = result.get('01', 0) + result.get('10', 0)
    
    # With high confidence, we expect almost all outcomes to be matching
    # Using a generous tolerance since sampling noise might be present
    assert matching / total > 0.9, f"Expected >90% matching outcomes, got {matching/total*100:.2f}%"
    assert non_matching / total < 0.1, f"Expected <10% non-matching outcomes, got {non_matching/total*100:.2f}%"


def test_bell_state_return_type_and_format():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    result = candidate()
    
    # Verify return type is dict
    assert isinstance(result, dict), "Function must return a dictionary"
    
    # Verify all values are integers (counts)
    for key, value in result.items():
        assert isinstance(key, str), f"Key must be string, got {type(key)}"
        assert isinstance(value, int), f"Value must be int (count), got {type(value)}"
        assert value > 0, f"Count must be positive, got {value}"
    
    # Verify keys are of the correct format (binary strings of length 2)
    for key in result.keys():
        assert len(key) == 2, f"Measurement key must be 2 bits, got {len(key)} bits in '{key}'"
        assert set(key).issubset({'0', '1'}), f"Measurement key must contain only '0' and '1', got '{key}'"