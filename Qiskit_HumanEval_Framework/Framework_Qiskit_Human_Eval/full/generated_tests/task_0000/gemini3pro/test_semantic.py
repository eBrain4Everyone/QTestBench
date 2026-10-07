# SEMANTIC tests — Qiskit HumanEval task task_0000
# Generated: 2026-04-28T11:36:48.919597
# Model: google/gemini-3.1-pro-preview (gemini3pro)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate(3)\n    assert isinstance(result, QuantumCircuit)\n    assert result.num_qubits == 3\n'
ENTRY_POINT_NAME = 'create_quantum_circuit'
# --- Official check block end ---
def test_create_circuit_1():
    import builtins as _b
    from qiskit import QuantumCircuit
    
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    n_qubits = 1
    result = candidate(n_qubits)
    
    assert isinstance(result, QuantumCircuit), f"Expected a QuantumCircuit object, but got {type(result)}."
    assert result.num_qubits == n_qubits, f"Expected circuit to have {n_qubits} qubit(s), but got {result.num_qubits}."

def test_create_circuit_2():
    import builtins as _b
    from qiskit import QuantumCircuit
    
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    n_qubits = 5
    result = candidate(n_qubits)
    
    assert isinstance(result, QuantumCircuit), f"Expected a QuantumCircuit object, but got {type(result)}."
    assert result.num_qubits == n_qubits, f"Expected circuit to have {n_qubits} qubit(s), but got {result.num_qubits}."

def test_create_circuit_3():
    import builtins as _b
    from qiskit import QuantumCircuit
    
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    n_qubits = 0
    result = candidate(n_qubits)
    
    assert isinstance(result, QuantumCircuit), f"Expected a QuantumCircuit object, but got {type(result)}."
    assert result.num_qubits == n_qubits, f"Expected circuit to have {n_qubits} qubit(s), but got {result.num_qubits}."