# SEMANTIC tests — Qiskit HumanEval task task_0020
# Generated: 2026-04-28T12:35:44.574476
# Model: openai/gpt-5.4 (gpt54)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    result.remove_final_measurements()\n    backend = FakePerth()\n    assert result.num_qubits == backend.num_qubits\n    assert result.layout.initial_index_layout()[:3] == [2, 4, 6]\n'
ENTRY_POINT_NAME = 'transpile_ghz_customlayout'
# --- Official check block end ---
def test_returns_quantum_circuit_and_uses_custom_layout_1():
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

    assert isinstance(qc, QuantumCircuit), "Function must return a QuantumCircuit instance."
    assert qc.num_qubits == FakePerth().num_qubits, "Transpiled circuit should be mapped onto the FakePerth backend qubit count."
    assert qc.num_clbits == 0, "Prompt specifies a GHZ circuit transpilation, not a measured circuit."

    layout = getattr(qc, "layout", None)
    assert layout is not None, "Transpiled circuit should carry layout information."

    initial_layout = None
    if hasattr(layout, "initial_layout"):
        initial_layout = layout.initial_layout
    elif hasattr(layout, "initial_index_layout"):
        initial_layout = layout

    assert initial_layout is not None, "Circuit layout should expose an initial layout."

    mapped = []
    for virt in range(3):
        phys = None
        try:
            phys = initial_layout[qc.qubits[virt]]
        except Exception:
            try:
                phys = initial_layout.get_physical_bits()[qc.qubits[virt]]
            except Exception:
                phys = None
        if phys is None:
            try:
                phys = layout.initial_index_layout()[virt]
            except Exception:
                pass
        mapped.append(phys)

    assert mapped == [2, 4, 6], f"Custom initial layout should map logical qubits to physical [2, 4, 6], got {mapped}."


def test_prepares_ghz_state_on_layout_qubits_2():
    import builtins as _b
    import numpy as np
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector, partial_trace
    from qiskit_ibm_runtime.fake_provider import FakePerth

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    qc = candidate()
    backend = FakePerth()

    assert qc.num_qubits == backend.num_qubits, "Returned circuit should be transpiled for the backend-sized register."

    sv = Statevector.from_instruction(qc)
    reduced = partial_trace(sv, [0, 1, 3, 5, 7])

    target = QuantumCircuit(3)
    target.h(0)
    target.cx(0, 1)
    target.cx(0, 2)
    target_sv = Statevector.from_instruction(target)

    reduced_dm = reduced.data
    target_dm = np.outer(target_sv.data, np.conjugate(target_sv.data))

    assert np.allclose(reduced_dm, target_dm, atol=1e-4, rtol=1e-5), (
        "Reduced state on physical qubits [2, 4, 6] should equal the 3-qubit GHZ state."
    )


def test_only_layout_qubits_are_nontrivial_and_entangled_3():
    import builtins as _b
    import numpy as np
    from qiskit.quantum_info import Statevector

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    qc = candidate()
    sv = Statevector.from_instruction(qc)
    probs = sv.probabilities_dict()

    nonzero = {k: v for k, v in probs.items() if v > 1e-10}
    assert len(nonzero) == 2, f"GHZ circuit should produce exactly two computational basis outcomes, got {list(nonzero.keys())}."

    keys = sorted(nonzero.keys())
    expected_keys = sorted(["00000000", "01010100"])
    assert keys == expected_keys, (
        f"With layout [2,4,6], nonzero basis states should be 00000000 and 01010100, got {keys}."
    )

    vals = [nonzero[k] for k in keys]
    assert np.allclose(vals, [0.5, 0.5], atol=1e-4, rtol=1e-5), (
        f"GHZ state should have equal probabilities 0.5 and 0.5 on its two basis components, got {vals}."
    )