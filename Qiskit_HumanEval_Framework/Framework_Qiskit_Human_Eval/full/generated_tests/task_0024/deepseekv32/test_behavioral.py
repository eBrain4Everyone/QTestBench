# BEHAVIORAL tests — Qiskit HumanEval task task_0024
# Generated: 2026-04-28T11:27:46.092221
# Model: deepseek/deepseek-v3.2 (deepseekv32)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    balanced = QuantumCircuit(5)\n    balanced.cx(3, 4)\n    assert candidate(balanced) == False\n    constant = QuantumCircuit(9)\n    constant.x(8)\n    assert candidate(constant) == True\n'
ENTRY_POINT_NAME = 'dj_algorithm'
# --- Official check block end ---
def test_constant_zero_oracle_1():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    from qiskit import QuantumCircuit
    # n = 2 input qubits, plus 1 output qubit
    oracle = QuantumCircuit(3)
    # constant 0: do nothing (identity)
    # Apply DJ algorithm
    result = candidate(oracle)
    assert result is True, f"Constant 0 oracle should return True, got {result}"

def test_constant_one_oracle_2():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    from qiskit import QuantumCircuit
    # n = 2 input qubits, plus 1 output qubit
    oracle = QuantumCircuit(3)
    # constant 1: flip the output qubit for all inputs
    oracle.x(2)
    result = candidate(oracle)
    assert result is True, f"Constant 1 oracle should return True, got {result}"

def test_balanced_oracle_3():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    from qiskit import QuantumCircuit
    # n = 2 input qubits, plus 1 output qubit
    oracle = QuantumCircuit(3)
    # balanced: output = parity of input qubits
    oracle.cx(0, 2)
    oracle.cx(1, 2)
    result = candidate(oracle)
    assert result is False, f"Balanced oracle should return False, got {result}"