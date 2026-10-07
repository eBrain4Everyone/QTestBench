# BEHAVIORAL tests — Qiskit HumanEval task task_0000
# Generated: 2026-04-28T12:38:53.402910
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
    
    circuit = candidate(2)
    assert isinstance(circuit, QuantumCircuit), "Function should return a QuantumCircuit instance"
    assert circuit.num_qubits == 2, "Circuit should have the specified number of qubits"
    assert circuit.num_clbits == 0, "Circuit should have no classical bits by default"


def test_create_quantum_circuit_single_qubit():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    circuit = candidate(1)
    assert isinstance(circuit, QuantumCircuit), "Function should return a QuantumCircuit instance"
    assert circuit.num_qubits == 1, "Circuit should have exactly 1 qubit"
    assert circuit.num_clbits == 0, "Circuit should have no classical bits"


def test_create_quantum_circuit_larger_circuit():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    n = 5
    circuit = candidate(n)
    assert isinstance(circuit, QuantumCircuit), "Function should return a QuantumCircuit instance"
    assert circuit.num_qubits == n, f"Circuit should have {n} qubits"
    assert circuit.num_clbits == 0, "Circuit should have no classical bits"
    assert circuit.qubits[0].register.name == "q", "Qubits should be named 'q'"