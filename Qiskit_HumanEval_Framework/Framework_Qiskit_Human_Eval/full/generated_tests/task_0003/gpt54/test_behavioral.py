# BEHAVIORAL tests — Qiskit HumanEval task task_0003
# Generated: 2026-04-28T12:34:40.362510
# Model: openai/gpt-5.4 (gpt54)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from qiskit.quantum_info import Statevector\n    import math\n    import matplotlib\n\n    def check_circuit(circuit):\n        assert circuit.data[-1].operation.name == "measure"\n        circuit.remove_final_measurements()\n        ghz_statevector = (\n            Statevector.from_label("000") + Statevector.from_label("111")\n        ) / math.sqrt(2)\n        assert Statevector.from_instruction(circuit).equiv(ghz_statevector)\n\n    circuit = candidate()\n    check_circuit(circuit)\n\n    circuit, drawing = candidate(drawing=True)\n    check_circuit(circuit)\n    assert isinstance(drawing, matplotlib.figure.Figure)\n'
ENTRY_POINT_NAME = 'create_ghz'
# --- Official check block end ---
def test_ghz_measurement_counts_1():
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
    assert isinstance(qc, QuantumCircuit), "create_ghz() should return a QuantumCircuit when drawing=False."
    assert qc.num_qubits == 3, "The GHZ circuit must act on exactly 3 qubits."
    assert qc.num_clbits == 3, "The GHZ circuit must include measurement into exactly 3 classical bits."

    measured = qc.remove_final_measurements(inplace=False)
    sv = Statevector.from_instruction(measured)
    probs = sv.probabilities_dict()

    assert set(probs.keys()).issubset({"000", "111"}), "A correct 3-qubit GHZ state should only have support on |000> and |111> before measurement."
    assert np.allclose(probs.get("000", 0.0), 0.5, atol=1e-4, rtol=1e-5), "The probability of measuring 000 should be 0.5 for a GHZ state."
    assert np.allclose(probs.get("111", 0.0), 0.5, atol=1e-4, rtol=1e-5), "The probability of measuring 111 should be 0.5 for a GHZ state."
    assert np.allclose(sum(probs.values()), 1.0, atol=1e-4, rtol=1e-5), "State probabilities should sum to 1."


def test_ghz_structure_and_measurements_2():
    import builtins as _b
    from qiskit import QuantumCircuit

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    qc = candidate(False)
    assert isinstance(qc, QuantumCircuit), "create_ghz(False) should return a QuantumCircuit."
    assert qc.num_qubits == 3, "The returned circuit must have 3 qubits."
    assert qc.num_clbits == 3, "The returned circuit must have 3 classical bits for measurement."

    ops = qc.data
    measure_ops = [inst for inst in ops if inst.operation.name == "measure"]
    assert len(measure_ops) == 3, "The GHZ circuit should measure all 3 qubits exactly once."

    non_measure_names = [inst.operation.name for inst in ops if inst.operation.name != "measure"]
    assert "h" in non_measure_names, "A GHZ circuit should include a Hadamard gate."
    assert non_measure_names.count("cx") >= 2, "A GHZ circuit should include at least two CNOT gates to entangle 3 qubits."

    assert all(inst.operation.name == "measure" for inst in ops[-3:]), "Measurements should appear at the end of the circuit."


def test_ghz_drawing_option_3():
    import builtins as _b
    import matplotlib.figure
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    result = candidate(True)
    assert isinstance(result, tuple), "create_ghz(True) should return a tuple of (circuit, drawing)."
    assert len(result) == 2, "create_ghz(True) should return exactly two items: the circuit and its drawing."

    qc, drawing = result
    assert isinstance(qc, QuantumCircuit), "The first item returned by create_ghz(True) must be a QuantumCircuit."
    assert isinstance(drawing, matplotlib.figure.Figure), "The second item returned by create_ghz(True) must be a Matplotlib Figure."

    measured = qc.remove_final_measurements(inplace=False)
    probs = Statevector.from_instruction(measured).probabilities_dict()
    assert set(probs.keys()).issubset({"000", "111"}), "The circuit returned with drawing=True must still prepare a GHZ state."
    assert abs(probs.get("000", 0.0) - 0.5) <= 1e-4, "The circuit returned with drawing=True should give probability 0.5 for 000."
    assert abs(probs.get("111", 0.0) - 0.5) <= 1e-4, "The circuit returned with drawing=True should give probability 0.5 for 111."