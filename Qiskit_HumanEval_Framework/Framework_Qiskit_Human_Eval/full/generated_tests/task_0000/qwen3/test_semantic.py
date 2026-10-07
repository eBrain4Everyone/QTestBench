# SEMANTIC tests — Qiskit HumanEval task task_0000
# Generated: 2026-04-28T12:38:47.562207
# Model: qwen/qwen3-coder-next (qwen3)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate(3)\n    assert isinstance(result, QuantumCircuit)\n    assert result.num_qubits == 3\n'
ENTRY_POINT_NAME = 'create_quantum_circuit'
# --- Official check block end ---
def test_create_quantum_circuit_basic():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    # Test with n_qubits = 1: should create a circuit with 1 qubit and 1 classical bit
    qc = candidate(1)
    assert qc.num_qubits == 1, f"Expected 1 qubit, got {qc.num_qubits}"
    assert qc.num_clbits == 1, f"Expected 1 classical bit, got {qc.num_clbits}"

def test_create_quantum_circuit_multi_qubits():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    # Test with n_qubits = 5: should create a circuit with 5 qubits and 5 classical bits
    qc = candidate(5)
    assert qc.num_qubits == 5, f"Expected 5 qubits, got {qc.num_qubits}"
    assert qc.num_clbits == 5, f"Expected 5 classical bits, got {qc.num_clbits}"

def test_create_quantum_circuit_zero_qubits():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    # Test with n_qubits = 0: should create a circuit with 0 qubits and 0 classical bits
    qc = candidate(0)
    assert qc.num_qubits == 0, f"Expected 0 qubits, got {qc.num_qubits}"
    assert qc.num_clbits == 0, f"Expected 0 classical bits, got {qc.num_clbits}"