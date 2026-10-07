# SEMANTIC tests — Qiskit HumanEval task task_0000
# Generated: 2026-04-28T12:26:32.957754
# Model: openai/gpt-5.4 (gpt54)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate(3)\n    assert isinstance(result, QuantumCircuit)\n    assert result.num_qubits == 3\n'
ENTRY_POINT_NAME = 'create_quantum_circuit'
# --- Official check block end ---
def test_returns_quantum_circuit_with_matching_qubit_count_1():
    import builtins as _b
    from qiskit import QuantumCircuit

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    n_qubits = 3
    qc = candidate(n_qubits)

    assert isinstance(qc, QuantumCircuit), "create_quantum_circuit should return a qiskit.QuantumCircuit instance."
    assert qc.num_qubits == n_qubits, "Returned circuit should have exactly the requested number of qubits."


def test_zero_qubits_creates_empty_circuit_2():
    import builtins as _b
    from qiskit import QuantumCircuit

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    qc = candidate(0)

    assert isinstance(qc, QuantumCircuit), "For n_qubits=0, the function should still return a QuantumCircuit."
    assert qc.num_qubits == 0, "For n_qubits=0, the returned circuit should contain zero qubits."
    assert qc.num_clbits == 0, "The prompt only specifies generating a quantum circuit; an empty zero-qubit circuit should have no classical bits by default."
    assert len(qc.data) == 0, "A zero-qubit circuit should be empty and contain no instructions."


def test_statevector_dimension_matches_requested_size_3():
    import builtins as _b
    import numpy as np
    from qiskit.quantum_info import Statevector

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    n_qubits = 4
    qc = candidate(n_qubits)
    sv = Statevector.from_instruction(qc)

    assert qc.num_qubits == n_qubits, "Returned circuit should preserve the requested qubit count."
    assert sv.data.shape == (2 ** n_qubits,), "Statevector dimension must match the number of qubits in the returned circuit."
    assert np.allclose(np.linalg.norm(sv.data), 1.0, atol=1e-4, rtol=1e-5), "Circuit must define a valid quantum evolution producing a normalized statevector."