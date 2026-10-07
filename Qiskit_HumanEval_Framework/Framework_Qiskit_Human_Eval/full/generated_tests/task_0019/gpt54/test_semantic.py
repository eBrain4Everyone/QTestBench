# SEMANTIC tests — Qiskit HumanEval task task_0019
# Generated: 2026-04-28T12:35:03.470711
# Model: openai/gpt-5.4 (gpt54)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    result.remove_final_measurements()\n    backend = FakeTorontoV2()\n    # Check initial layout is not the trivial layout (this is very unlikely\n    # if transpiled with optimization level 3)\n    assert result.layout.initial_index_layout() != list(range(backend.num_qubits))\n    # Optimization level 3 should easily find circuits with depth < 200\n    assert result.depth() < 150\n'
ENTRY_POINT_NAME = 'transpile_circuit_maxopt'
# --- Official check block end ---
def test_returns_transpiled_circuit_on_fake_toronto_1():
    import builtins as _b
    import numpy as np
    from qiskit import QuantumCircuit
    from qiskit_ibm_runtime.fake_provider import FakeTorontoV2
    from qiskit.transpiler import CouplingMap

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    qc = candidate()

    assert isinstance(qc, QuantumCircuit), "Function must return a QuantumCircuit instance."
    assert qc.num_qubits == 11, "Returned circuit must act on 11 qubits for the 11-qubit GHZ circuit."
    assert qc.num_clbits == 0, "Prompt specifies a circuit, not a measured/classical-register circuit."

    backend = FakeTorontoV2()
    backend_qubits = backend.num_qubits
    assert qc.num_qubits <= backend_qubits, "Returned circuit must be mappable to the FakeTorontoV2 backend size."

    cmap = CouplingMap(backend.coupling_map)
    for inst in qc.data:
        op = inst.operation
        qargs = inst.qubits
        if len(qargs) == 2:
            q0 = qc.find_bit(qargs[0]).index
            q1 = qc.find_bit(qargs[1]).index
            edge_ok = cmap.graph.has_edge(q0, q1) or cmap.graph.has_edge(q1, q0)
            assert edge_ok, f"Two-qubit gate {op.name} on qubits {(q0, q1)} must respect FakeTorontoV2 coupling map."


def test_preserves_ghz_state_semantics_2():
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

    ref = QuantumCircuit(11)
    ref.h(0)
    for i in range(10):
        ref.cx(i, i + 1)

    sv_ref = Statevector.from_instruction(ref)
    sv_out = Statevector.from_instruction(qc)

    overlap = np.vdot(sv_ref.data, sv_out.data)
    fidelity = float(np.abs(overlap) ** 2)
    assert np.allclose(fidelity, 1.0, atol=1e-4, rtol=1e-5), (
        f"Returned circuit must be equivalent to an 11-qubit GHZ preparation circuit; fidelity was {fidelity}."
    )

    probs = sv_out.probabilities_dict()
    assert len(probs) == 2, "GHZ state should have support on exactly two computational basis states."
    p0 = probs.get("0" * 11, 0.0)
    p1 = probs.get("1" * 11, 0.0)
    assert np.allclose(p0, 0.5, atol=1e-4, rtol=1e-5), "GHZ state must give probability 0.5 for all-zeros."
    assert np.allclose(p1, 0.5, atol=1e-4, rtol=1e-5), "GHZ state must give probability 0.5 for all-ones."


def test_uses_backend_basis_and_shows_transpilation_effect_3():
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
    target = backend.target
    basis_names = set(target.operation_names)

    for inst in qc.data:
        opname = inst.operation.name
        assert opname in basis_names, (
            f"Transpiled circuit should use operations supported by FakeTorontoV2; found unsupported op '{opname}'."
        )

    original = QuantumCircuit(11)
    original.h(0)
    for i in range(10):
        original.cx(i, i + 1)

    changed = (
        qc.count_ops() != original.count_ops()
        or any(qc.find_bit(q).index != i for i, q in enumerate(qc.qubits))
        or any(inst.operation.name not in {"h", "cx"} for inst in qc.data)
    )
    assert changed, (
        "Function should return a transpiled/mapped circuit for FakeTorontoV2, not merely the original abstract GHZ circuit."
    )