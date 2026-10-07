# BEHAVIORAL tests — Qiskit HumanEval task task_0024
# Generated: 2026-04-28T12:03:54.892509
# Model: google/gemini-3.1-pro-preview (gemini3pro)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    balanced = QuantumCircuit(5)\n    balanced.cx(3, 4)\n    assert candidate(balanced) == False\n    constant = QuantumCircuit(9)\n    constant.x(8)\n    assert candidate(constant) == True\n'
ENTRY_POINT_NAME = 'dj_algorithm'
# --- Official check block end ---
def test_constant_zero_1():
    import builtins as _b
    from qiskit import QuantumCircuit
    
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    dj_algorithm = g[entry]
    
    # 1 input qubit, 1 output qubit (ancilla)
    # f(x) = 0 is an identity circuit
    qc = QuantumCircuit(2)
    
    res = dj_algorithm(qc)
    assert res == True, "Failed to identify 1-input constant f(x)=0 oracle as constant."

def test_constant_one_2():
    import builtins as _b
    from qiskit import QuantumCircuit
    
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    dj_algorithm = g[entry]
    
    # 4 input qubits, 1 output qubit (ancilla)
    # f(x) = 1 applies X to the output qubit
    qc = QuantumCircuit(5)
    qc.x(4)
    
    res = dj_algorithm(qc)
    assert res == True, "Failed to identify 4-input constant f(x)=1 oracle as constant."

def test_balanced_3():
    import builtins as _b
    from qiskit import QuantumCircuit
    
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    dj_algorithm = g[entry]
    
    # 4 input qubits, 1 output qubit (ancilla)
    # A balanced function flips the output for half the inputs
    qc = QuantumCircuit(5)
    qc.cx(0, 4)
    qc.cx(2, 4)
    qc.cx(3, 4)
    
    res = dj_algorithm(qc)
    assert res == False, "Failed to identify balanced oracle as balanced."