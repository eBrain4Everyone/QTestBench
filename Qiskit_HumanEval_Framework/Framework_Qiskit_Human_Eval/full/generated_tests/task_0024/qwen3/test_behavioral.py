# BEHAVIORAL tests — Qiskit HumanEval task task_0024
# Generated: 2026-04-28T12:41:38.169415
# Model: qwen/qwen3-coder-next (qwen3)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    balanced = QuantumCircuit(5)\n    balanced.cx(3, 4)\n    assert candidate(balanced) == False\n    constant = QuantumCircuit(9)\n    constant.x(8)\n    assert candidate(constant) == True\n'
ENTRY_POINT_NAME = 'dj_algorithm'
# --- Official check block end ---
def test_dj_algorithm_constant_oracle_1():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    # Create a constant oracle (always returns 0)
    n = 3
    oracle = QuantumCircuit(n + 1)
    # Do nothing: output qubit stays |0>, so f(x)=0 for all x (constant)
    
    result = candidate(oracle)
    assert result is True, "Constant oracle (f(x)=0) should return True"


def test_dj_algorithm_constant_oracle_2():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    # Create a constant oracle (always returns 1)
    n = 3
    oracle = QuantumCircuit(n + 1)
    oracle.x(n)  # Flip output qubit to |1>, so f(x)=1 for all x (constant)
    
    result = candidate(oracle)
    assert result is True, "Constant oracle (f(x)=1) should return True"


def test_dj_algorithm_balanced_oracle():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    # Create a balanced oracle (e.g., f(x) = x0 XOR x1 XOR ... XOR x_{n-1})
    n = 3
    oracle = QuantumCircuit(n + 1)
    # Apply CNOTs from each input qubit to the output qubit
    for i in range(n):
        oracle.cx(i, n)
    
    result = candidate(oracle)
    assert result is False, "Balanced oracle should return False"