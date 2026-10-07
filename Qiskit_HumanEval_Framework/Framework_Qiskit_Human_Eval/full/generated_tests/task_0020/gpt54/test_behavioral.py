# BEHAVIORAL tests — Qiskit HumanEval task task_0020
# Generated: 2026-04-28T12:35:59.944190
# Model: openai/gpt-5.4 (gpt54)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    result.remove_final_measurements()\n    backend = FakePerth()\n    assert result.num_qubits == backend.num_qubits\n    assert result.layout.initial_index_layout()[:3] == [2, 4, 6]\n'
ENTRY_POINT_NAME = 'transpile_ghz_customlayout'
# --- Official check block end ---
def test_customlayout_mapping_1():
    import builtins as _b
    import numpy as np
    from qiskit import QuantumCircuit
    from qiskit_ibm_runtime.fake_provider import FakePerth

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    qc = candidate()
    assert isinstance(qc, QuantumCircuit), "The function must return a QuantumCircuit instance."

    backend = FakePerth()
    layout = getattr(qc, "layout", None)
    assert layout is not None, "The transpiled circuit should carry layout information."

    initial_layout = getattr(layout, "initial_layout", None)
    assert initial_layout is not None, "The transpiled circuit should include an initial layout."

    virt_to_phys = {}
    for virt, phys in initial_layout.get_virtual_bits().items():
        if hasattr(virt, "_index"):
            virt_to_phys[int(virt._index)] = int(phys)

    assert len(virt_to_phys) >= 3, "Initial layout should map at least the three logical qubits."
    expected = {0: 2, 1: 4, 2: 6}
    for q, p in expected.items():
        assert virt_to_phys.get(q) == p, f"Logical qubit {q} should be initially mapped to physical qubit {p}, got {virt_to_phys.get(q)} instead."

    assert qc.num_qubits == backend.num_qubits, "A transpiled circuit for the backend should be expanded to the backend qubit count."


def test_ghz_state_behavior_2():
    import builtins as _b
    import numpy as np
    from qiskit.quantum_info import Statevector, partial_trace

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    qc = candidate()
    qc_nom = qc.remove_final_measurements(inplace=False)
    sv = Statevector.from_instruction(qc_nom)

    probs = sv.probabilities_dict()
    nz = {k: v for k, v in probs.items() if v > 1e-9}
    assert len(nz) == 2, f"A 3-qubit GHZ state on some mapped qubits should have exactly two nonzero computational basis outcomes, got {nz}."

    vals = sorted(nz.values())
    assert np.allclose(vals, [0.5, 0.5], atol=1e-4, rtol=1e-5), f"The two GHZ basis outcomes should each have probability 0.5, got {vals}."

    keys = list(nz.keys())
    diff_positions = [i for i, (a, b) in enumerate(zip(keys[0], keys[1])) if a != b]
    assert len(diff_positions) == 3, f"The two GHZ outcomes should differ in exactly three qubit positions, indicating entanglement across three qubits; got differing positions {diff_positions}."

    reduced = partial_trace(sv, [i for i in range(qc.num_qubits) if i not in diff_positions])
    purity = np.real(np.trace(reduced.data @ reduced.data))
    assert np.allclose(purity, 0.5, atol=1e-4, rtol=1e-5), f"The reduced state on the GHZ qubits should be a rank-2 mixed state with purity 0.5, got {purity}."


def test_backend_compatibility_and_ops_3():
    import builtins as _b
    from qiskit import transpile
    from qiskit_ibm_runtime.fake_provider import FakePerth

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    qc = candidate()
    backend = FakePerth()

    for inst, qargs, cargs in qc.data:
        opname = inst.name
        if opname == "barrier":
            continue
        assert opname in backend.operation_names, f"Operation '{opname}' is not supported by FakePerth."

    ops = qc.count_ops()
    two_qubit_total = sum(count for name, count in ops.items() if name in {"cx", "ecr", "cz"})
    assert two_qubit_total >= 2, f"A mapped 3-qubit GHZ circuit should require at least two entangling operations, got operations {dict(ops)}."

    h_like_total = sum(count for name, count in ops.items() if name in {"h", "sx", "rz", "x", "u", "u1", "u2", "u3"})
    assert h_like_total >= 1, f"A GHZ preparation should include at least one single-qubit basis-change operation, got operations {dict(ops)}."

    assert qc.num_clbits == 0 or qc.num_clbits == 3, f"The returned circuit should either be purely quantum or measure the three GHZ qubits, got {qc.num_clbits} classical bits."