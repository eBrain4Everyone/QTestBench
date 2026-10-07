# SEMANTIC tests — Qiskit HumanEval task task_0003
# Generated: 2026-04-28T12:34:25.542160
# Model: openai/gpt-5.4 (gpt54)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from qiskit.quantum_info import Statevector\n    import math\n    import matplotlib\n\n    def check_circuit(circuit):\n        assert circuit.data[-1].operation.name == "measure"\n        circuit.remove_final_measurements()\n        ghz_statevector = (\n            Statevector.from_label("000") + Statevector.from_label("111")\n        ) / math.sqrt(2)\n        assert Statevector.from_instruction(circuit).equiv(ghz_statevector)\n\n    circuit = candidate()\n    check_circuit(circuit)\n\n    circuit, drawing = candidate(drawing=True)\n    check_circuit(circuit)\n    assert isinstance(drawing, matplotlib.figure.Figure)\n'
ENTRY_POINT_NAME = 'create_ghz'
# --- Official check block end ---
def test_ghz_circuit_structure_and_measurement_1():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    from qiskit import QuantumCircuit

    qc = candidate()
    assert isinstance(qc, QuantumCircuit), "create_ghz() should return a QuantumCircuit when drawing=False."
    assert qc.num_qubits == 3, "The returned circuit must act on exactly 3 qubits."
    assert qc.num_clbits == 3, "The returned circuit must include 3 classical bits for measurement."

    ops = qc.count_ops()
    assert ops.get("h", 0) == 1, "A GHZ circuit should contain exactly one Hadamard gate."
    assert ops.get("cx", 0) == 2, "A 3-qubit GHZ circuit should contain exactly two CX gates."
    assert ops.get("measure", 0) == 3, "The circuit must measure all 3 qubits."

    measured_qubits = set()
    measured_clbits = set()
    for inst, qargs, cargs in qc.data:
        if inst.name == "measure":
            measured_qubits.add(qc.find_bit(qargs[0]).index)
            measured_clbits.add(qc.find_bit(cargs[0]).index)

    assert measured_qubits == {0, 1, 2}, "All three qubits must be measured."
    assert measured_clbits == {0, 1, 2}, "Measurements should write into all three classical bits."


def test_ghz_statevector_before_measurements_2():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    import numpy as np
    from qiskit.quantum_info import Statevector

    qc = candidate()

    no_measure = qc.remove_final_measurements(inplace=False)
    sv = Statevector.from_instruction(no_measure).data

    expected = np.zeros(8, dtype=complex)
    expected[0] = 1 / np.sqrt(2)
    expected[7] = 1 / np.sqrt(2)

    phase = 1.0
    idx = int(np.argmax(np.abs(expected)))
    if abs(sv[idx]) > 1e-12:
        phase = sv[idx] / expected[idx]
    aligned = sv / phase

    assert np.allclose(aligned, expected, atol=1e-4, rtol=1e-5), (
        "Ignoring global phase, the unmeasured circuit must prepare the 3-qubit GHZ state "
        "(|000> + |111>)/sqrt(2)."
    )


def test_ghz_drawing_and_output_distribution_3():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    from qiskit import transpile
    from qiskit_aer import AerSimulator

    result = candidate(drawing=True)
    assert isinstance(result, tuple) and len(result) == 2, (
        "create_ghz(drawing=True) should return a 2-tuple of (QuantumCircuit, drawing_object)."
    )
    qc, drawing = result
    assert qc.num_qubits == 3, "When drawing=True, the first returned item must still be a 3-qubit circuit."
    assert drawing is not None, "When drawing=True, the second returned item should be a non-None circuit drawing."

    backend = AerSimulator(seed_simulator=123)
    tqc = transpile(qc, backend, seed_transpiler=123)
    counts = backend.run(tqc, shots=1024).result().get_counts()

    allowed = {"000", "111"}
    observed = set(counts.keys())
    assert observed.issubset(allowed), (
        f"Measured GHZ outcomes should only be '000' or '111', but observed {observed}."
    )

    p000 = counts.get("000", 0) / 1024
    p111 = counts.get("111", 0) / 1024
    assert abs((p000 + p111) - 1.0) < 1e-9, "All shots should be accounted for by outcomes '000' and '111'."
    assert abs(p000 - 0.5) < 0.15 and abs(p111 - 0.5) < 0.15, (
        "The GHZ measurement distribution should be approximately balanced between '000' and '111'."
    )