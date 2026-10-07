# BEHAVIORAL tests — Qiskit HumanEval task task_0000
# Generated: 2026-04-28T12:26:43.459817
# Model: openai/gpt-5.4 (gpt54)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate(3)\n    assert isinstance(result, QuantumCircuit)\n    assert result.num_qubits == 3\n'
ENTRY_POINT_NAME = 'create_quantum_circuit'
# --- Official check block end ---
def test_returns_quantum_circuit_with_requested_qubit_count_1():
    import builtins as _b
    from qiskit import QuantumCircuit

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    n = 3
    qc = candidate(n)

    assert isinstance(qc, QuantumCircuit), "create_quantum_circuit should return a qiskit.QuantumCircuit instance."
    assert qc.num_qubits == n, f"Returned circuit should have exactly {n} qubits, but has {qc.num_qubits}."
    assert qc.num_clbits == 0, f"Returned circuit should not add classical bits unless requested, but has {qc.num_clbits}."


def test_handles_zero_qubits_and_empty_circuit_2():
    import builtins as _b
    from qiskit import QuantumCircuit

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    qc = candidate(0)

    assert isinstance(qc, QuantumCircuit), "For n_qubits=0, the function should still return a QuantumCircuit instance."
    assert qc.num_qubits == 0, f"For n_qubits=0, circuit should contain 0 qubits, but has {qc.num_qubits}."
    assert len(qc.data) == 0, f"For an empty circuit request, the circuit should contain no operations, but has {len(qc.data)}."


def test_distinct_sizes_produce_matching_circuit_sizes_3():
    import builtins as _b
    from qiskit import QuantumCircuit

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    sizes = [1, 2, 5]
    circuits = [candidate(n) for n in sizes]

    for n, qc in zip(sizes, circuits):
        assert isinstance(qc, QuantumCircuit), f"Result for n_qubits={n} should be a QuantumCircuit instance."
        assert qc.num_qubits == n, f"Result for n_qubits={n} should have {n} qubits, but has {qc.num_qubits}."

    assert circuits[0] is not circuits[1] and circuits[1] is not circuits[2] and circuits[0] is not circuits[2], \
        "Each call should return a distinct QuantumCircuit object, not reuse the same instance."