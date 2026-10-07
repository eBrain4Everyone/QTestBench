# SEMANTIC tests — Qiskit HumanEval task task_0024
# Generated: 2026-04-28T12:03:24.703649
# Model: google/gemini-3.1-pro-preview (gemini3pro)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    balanced = QuantumCircuit(5)\n    balanced.cx(3, 4)\n    assert candidate(balanced) == False\n    constant = QuantumCircuit(9)\n    constant.x(8)\n    assert candidate(constant) == True\n'
ENTRY_POINT_NAME = 'dj_algorithm'
# --- Official check block end ---
def test_dj_algorithm_1():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    dj_algorithm = g[entry]

    from qiskit import QuantumCircuit
    
    # Constant oracle f(x) = 0 on 2 input qubits, 1 output qubit
    oracle = QuantumCircuit(3)
    
    result = dj_algorithm(oracle)
    assert result is True, "Expected True for a constant oracle f(x)=0"

def test_dj_algorithm_2():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    dj_algorithm = g[entry]

    from qiskit import QuantumCircuit
    
    # Balanced oracle f(x) = x_0 XOR x_1 on 3 input qubits, 1 output qubit
    oracle = QuantumCircuit(4)
    oracle.cx(0, 3)
    oracle.cx(1, 3)
    
    result = dj_algorithm(oracle)
    assert result is False, "Expected False for a balanced oracle"

def test_dj_algorithm_3():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    dj_algorithm = g[entry]

    from qiskit import QuantumCircuit
    
    # Constant oracle f(x) = 1 on 1 input qubit, 1 output qubit
    oracle = QuantumCircuit(2)
    oracle.x(1)
    
    result = dj_algorithm(oracle)
    assert result is True, "Expected True for a constant oracle f(x)=1"