# SEMANTIC tests — Qiskit HumanEval task task_0001
# Generated: 2026-04-28T11:38:31.970553
# Model: google/gemini-3.1-pro-preview (gemini3pro)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    assert isinstance(result, dict)\n    assert result.keys() == {"00", "11"}\n    assert 0.4 < (result["00"] / sum(result.values())) < 0.6\n'
ENTRY_POINT_NAME = 'run_bell_state_simulator'
# --- Official check block end ---
def test_return_type_and_keys_1():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    counts = candidate()
    
    assert isinstance(counts, dict), f"The return value must be a dictionary, got {type(counts)}"
    assert len(counts) > 0, "The counts dictionary should not be empty."
    
    for k, v in counts.items():
        assert isinstance(k, (str, int)), f"Keys should be string or int, got {type(k)}: {k}"
        if isinstance(k, str):
            if k.startswith('0x'):
                try:
                    int(k, 16)
                except ValueError:
                    assert False, f"Invalid hex string key: {k}"
            else:
                assert set(k).issubset({'0', '1', ' '}), f"String keys should be bitstrings or hex, got {k}"
        assert isinstance(v, (int, float)), f"Values should be int or float, got {type(v)}: {v}"

def test_bell_state_distribution_2():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    counts = candidate()
    total = sum(counts.values())
    assert total > 0, "Total counts must be greater than 0."
    
    prob_00 = 0
    prob_11 = 0
    for k, v in counts.items():
        if isinstance(k, int):
            if k == 0:
                prob_00 += v / total
            elif k == 3:
                prob_11 += v / total
        elif isinstance(k, str):
            if k.startswith('0x'):
                val = int(k, 16)
                if val == 0:
                    prob_00 += v / total
                elif val == 3:
                    prob_11 += v / total
            else:
                clean_k = k.replace(' ', '').lstrip('0')
                if clean_k == '':
                    prob_00 += v / total
                elif clean_k == '11':
                    prob_11 += v / total
                    
    assert prob_00 + prob_11 > 0.95, f"Expected '00' and '11' to dominate the distribution (Phi+ Bell state), got prob_00={prob_00}, prob_11={prob_11}"

def test_bell_state_balance_3():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    counts = candidate()
    total = sum(counts.values())
    assert total > 0, "Total counts must be greater than 0."
    
    prob_00 = 0
    prob_11 = 0
    for k, v in counts.items():
        if isinstance(k, int):
            if k == 0:
                prob_00 += v / total
            elif k == 3:
                prob_11 += v / total
        elif isinstance(k, str):
            if k.startswith('0x'):
                val = int(k, 16)
                if val == 0:
                    prob_00 += v / total
                elif val == 3:
                    prob_11 += v / total
            else:
                clean_k = k.replace(' ', '').lstrip('0')
                if clean_k == '':
                    prob_00 += v / total
                elif clean_k == '11':
                    prob_11 += v / total
                    
    assert 0.35 < prob_00 < 0.65, f"Expected prob_00 to be around 0.5 for balanced Bell state, got {prob_00}"
    assert 0.35 < prob_11 < 0.65, f"Expected prob_11 to be around 0.5 for balanced Bell state, got {prob_11}"