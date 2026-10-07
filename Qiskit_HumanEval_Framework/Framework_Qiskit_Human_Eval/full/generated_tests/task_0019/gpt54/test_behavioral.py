# BEHAVIORAL tests — Qiskit HumanEval task task_0019
# Generated: 2026-04-28T12:35:16.182090
# Model: openai/gpt-5.4 (gpt54)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    result.remove_final_measurements()\n    backend = FakeTorontoV2()\n    # Check initial layout is not the trivial layout (this is very unlikely\n    # if transpiled with optimization level 3)\n    assert result.layout.initial_index_layout() != list(range(backend.num_qubits))\n    # Optimization level 3 should easily find circuits with depth < 200\n    assert result.depth() < 150\n'
ENTRY_POINT_NAME = 'transpile_circuit_maxopt'
# --- Official check block end ---
def test_returns_quantum_circuit_1():
    import builtins as _b
    from qiskit import QuantumCircuit

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    qc = candidate()

    assert isinstance(qc, QuantumCircuit), "The function must return a Qiskit QuantumCircuit instance."
    assert qc.num_qubits == 11, f"The transpiled GHZ circuit must act on 11 qubits, got {qc.num_qubits}."
    assert qc.num_clbits == 0, f"The prompt does not require measurements; expected 0 classical bits, got {qc.num_clbits}."


def test_unitary_preserves_ghz_state_2():
    import builtins as _b
    import numpy as np
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    qc = candidate()

    assert isinstance(qc, QuantumCircuit), "The function must return a QuantumCircuit before checking state equivalence."
    assert qc.num_qubits == 11, f"Expected an 11-qubit circuit, got {qc.num_qubits}."

    evolved = Statevector.from_instruction(qc).data

    ref = QuantumCircuit(11)
    ref.h(0)
    for i in range(10):
        ref.cx(i, i + 1)
    target = Statevector.from_instruction(ref).data

    overlap = abs(np.vdot(target, evolved))
    assert np.allclose(overlap, 1.0, atol=1e-4, rtol=1e-5), (
        f"The returned circuit should be functionally equivalent to an 11-qubit GHZ preparation up to global phase; overlap was {overlap}."
    )

    significant = np.where(np.abs(evolved) > 1e-6)[0]
    assert len(significant) == 2, (
        f"A GHZ state should have support on exactly two computational basis states; found {len(significant)} significant amplitudes."
    )


def test_mapped_to_fake_toronto_and_optimized_3():
    import builtins as _b
    from qiskit import QuantumCircuit
    from qiskit_ibm_runtime.fake_provider import FakeTorontoV2

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    qc = candidate()
    backend = FakeTorontoV2()

    assert isinstance(qc, QuantumCircuit), "The function must return a QuantumCircuit before backend mapping checks."
    assert qc.layout is not None, "A transpiled circuit for a backend should carry layout information showing qubit mapping."
    assert qc.num_qubits == 11, f"Expected 11 qubits after transpilation, got {qc.num_qubits}."

    basis = set(backend.operation_names)
    circuit_ops = {instruction.operation.name for instruction in qc.data}
    unsupported = sorted(op for op in circuit_ops if op not in basis)
    assert not unsupported, (
        f"All operations in the transpiled circuit should be supported by FakeTorontoV2; unsupported operations found: {unsupported}."
    )

    two_qubit_ops = [
        instruction.operation.name
        for instruction in qc.data
        if getattr(instruction.operation, "num_qubits", 0) == 2
    ]
    assert len(two_qubit_ops) > 0, "A mapped GHZ circuit should contain at least one two-qubit entangling gate."
    assert len(two_qubit_ops) <= 10, (
        f"With maximum optimization, an 11-qubit GHZ preparation should not require more than 10 two-qubit gates; got {len(two_qubit_ops)}."
    )