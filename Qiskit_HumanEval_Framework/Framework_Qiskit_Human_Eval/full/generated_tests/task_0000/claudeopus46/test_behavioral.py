# BEHAVIORAL tests — Qiskit HumanEval task task_0000
# Generated: 2026-04-28T11:08:41.984618
# Model: anthropic/claude-opus-4-6 (claudeopus46)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate(3)\n    assert isinstance(result, QuantumCircuit)\n    assert result.num_qubits == 3\n'
ENTRY_POINT_NAME = 'create_quantum_circuit'
# --- Official check block end ---
def test_create_quantum_circuit_1():
    """Test that the function returns a QuantumCircuit with the correct number of qubits for n_qubits=1."""
    import builtins as _b
    from qiskit import QuantumCircuit

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    result = candidate(1)
    assert isinstance(result, QuantumCircuit), (
        f"Expected return type QuantumCircuit, got {type(result)}"
    )
    assert result.num_qubits == 1, (
        f"Expected 1 qubit, got {result.num_qubits}"
    )


def test_create_quantum_circuit_2():
    """Test that the function returns a QuantumCircuit with the correct number of qubits for various values."""
    import builtins as _b
    from qiskit import QuantumCircuit

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT