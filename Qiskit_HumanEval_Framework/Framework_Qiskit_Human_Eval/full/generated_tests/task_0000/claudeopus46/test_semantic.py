# SEMANTIC tests — Qiskit HumanEval task task_0000
# Generated: 2026-04-28T11:07:50.286237
# Model: anthropic/claude-opus-4-6 (claudeopus46)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate(3)\n    assert isinstance(result, QuantumCircuit)\n    assert result.num_qubits == 3\n'
ENTRY_POINT_NAME = 'create_quantum_circuit'
# --- Official check block end ---
def test_create_quantum_circuit_returns_correct_type_1():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    from qiskit import QuantumCircuit

    result = candidate(3)
    assert isinstance(result, QuantumCircuit), (
        f"Expected a QuantumCircuit instance, got {type(result)}"
    )
    assert result.num_qubits == 3, (
        f"Expected 3 qubits, got {result.num_qubits}"
    )


def test_create_quantum_circuit_various_sizes_2():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    from qiskit import QuantumCircuit

    for n in [1, 2, 5, 10]:
        result = candidate(n)
        assert isinstance(result, QuantumCircuit), (
            f"For n_qubits={n}, expected QuantumCircuit, got {type(result)}"
        )
        assert result.num_qubits == n, (
            f"For n_qubits={n}, expected {n} qubits, got {result.num_qubits}"
        )


def test_create_quantum_circuit_initial_state_3():
    import builtins as _b
    import numpy as np
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    from qiskit.quantum_info import Statevector

    n = 4
    qc = candidate(n)
    # A freshly created circuit with no gates should be in the |0...0> state
    sv = Statevector.from_instruction(qc)
    expected = np.zeros(2**n, dtype=complex)
    expected[0] = 1.0
    assert np.allclose(sv.data, expected, atol=1e-4, rtol=1e-5), (
        f"Expected |0000> state for a fresh {n}-qubit circuit, got {sv.data}"
    )