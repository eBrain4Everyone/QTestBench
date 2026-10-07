# BEHAVIORAL tests — Qiskit HumanEval task task_0001
# Generated: 2026-04-28T11:39:25.450907
# Model: google/gemini-3.1-pro-preview (gemini3pro)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    assert isinstance(result, dict)\n    assert result.keys() == {"00", "11"}\n    assert 0.4 < (result["00"] / sum(result.values())) < 0.6\n'
ENTRY_POINT_NAME = 'run_bell_state_simulator'
# --- Official check block end ---
def test_valid_return_and_keys_1():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    counts = candidate()
    assert isinstance(counts, dict), f"Expected a dictionary, got {type(counts).__name__}"
    
    str_keys = {str(k).replace(' ', '') for k in counts.keys()}
    assert ('00' in str_keys or '0' in str_keys) and ('11' in str_keys or '3' in str_keys), \
        f"Missing '00' or '11' in counts keys. Got: {counts.keys()}"

def test_bell_state_distribution_2():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    counts = candidate()
    assert isinstance(counts, dict), "Result is not a dictionary"
    
    normalized_counts = {str(k).replace(' ', ''): v for k, v in counts.items()}
    total = sum(normalized_counts.values())
    assert total > 0, "Sum of counts must be greater than 0"
    
    c_00 = normalized_counts.get('00', normalized_counts.get('0', 0))
    c_11 = normalized_counts.get('11', normalized_counts.get('3', 0))
    
    p_00 = c_00 / total
    p_11 = c_11 / total
    
    assert 0.3 <= p_00 <= 0.7, f"Expected proportion of '00' around 0.5, got {p_00}"
    assert 0.3 <= p_11 <= 0.7, f"Expected proportion of '11' around 0.5, got {p_11}"

def test_no_unexpected_states_3():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    counts = candidate()
    assert isinstance(counts, dict), "Result is not a dictionary"
    
    str_keys = {str(k).replace(' ', '') for k in counts.keys()}
    allowed = {'00', '11', '0', '3'}
    spurious = str_keys - allowed
    
    normalized_counts = {str(k).replace(' ', ''): v for k, v in counts.items()}
    total = sum(normalized_counts.values())
    
    if spurious and total > 0:
        spurious_prob = sum(normalized_counts[k] for k in spurious) / total
        assert spurious_prob < 0.05, f"Found unexpected states with non-negligible probability: {spurious}. Counts: {counts}"