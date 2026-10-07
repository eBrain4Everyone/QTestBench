# BEHAVIORAL tests — Qiskit HumanEval task task_0003
# Generated: 2026-04-28T11:10:57.974753
# Model: anthropic/claude-opus-4-6 (claudeopus46)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from qiskit.quantum_info import Statevector\n    import math\n    import matplotlib\n\n    def check_circuit(circuit):\n        assert circuit.data[-1].operation.name == "measure"\n        circuit.remove_final_measurements()\n        ghz_statevector = (\n            Statevector.from_label("000") + Statevector.from_label("111")\n        ) / math.sqrt(2)\n        assert Statevector.from_instruction(circuit).equiv(ghz_statevector)\n\n    circuit = candidate()\n    check_circuit(circuit)\n\n    circuit, drawing = candidate(drawing=True)\n    check_circuit(circuit)\n    assert isinstance(drawing, matplotlib.figure.Figure)\n'
ENTRY_POINT_NAME = 'create_ghz'
# --- Official check block end ---
def test_create_ghz_returns_circuit_1():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    from qiskit import QuantumCircuit

    result = candidate(drawing=False)
    assert isinstance(result, QuantumCircuit), \
        f"Expected QuantumCircuit when drawing=False, got {type(result)}"
    assert result.num_qubits == 3, \
        f"Expected 3 qubits, got {result.num_qubits}"
    # Check that measurements are present
    op_names = [inst.operation.name for inst in result.data]
    assert "measure" in op_names, \
        "Circuit should contain measurement operations"
    assert result.num_clbits >= 3, \
        f"Expected at least 3 classical bits for measurement, got {result.num_clbits}"


def test_create_ghz_statevector_2():
    import builtins as _b
    import numpy as np
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector

    circuit = candidate(drawing=False)

    # Remove measurements to get statevector
    circ_no_meas = QuantumCircuit(circuit.num_qubits)
    for inst in circuit.data:
        if inst.operation.name != "measure" and inst.operation.name != "barrier":
            circ_no_meas.append(inst.operation, inst.qubits)

    sv = Statevector.from_instruction(circ_no_meas)
    probs = sv.probabilities_dict()

    # GHZ state: should only have |000> and |111> with equal probability ~0.5
    assert "000" in probs, "GHZ state should have |000> component"
    assert "111" in probs, "GHZ state should have |111> component"
    assert np.isclose(probs.get("000", 0), 0.5, atol=1e-6), \
        f"Probability of |000> should be 0.5, got {probs.get('000', 0)}"
    assert np.isclose(probs.get("111", 0), 0.5, atol=1e-6), \
        f"Probability of |111> should be 0.5, got {probs.get('111', 0)}"

    # All other states should have zero probability
    for key, val in probs.items():
        if key not in ("000", "111"):
            assert np.isclose(val, 0.0, atol=1e-6), \
                f"State |{key}> should have 0 probability in GHZ, got {val}"


def test_create_ghz_drawing_returns_tuple_3():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    import matplotlib
    matplotlib.use("Agg")  # non-interactive backend
    import matplotlib.pyplot as plt
    from qiskit import QuantumCircuit

    result = candidate(drawing=True)

    # When drawing=True, should return both circuit and figure
    assert isinstance(result, (tuple, list)), \
        f"Expected tuple/list when drawing=True, got {type(result)}"
    assert len(result) == 2, \
        f"Expected 2 elements (circuit, figure), got {len(result)}"

    circ, fig = result
    assert isinstance(circ, QuantumCircuit), \
        f"First element should be QuantumCircuit, got {type(circ)}"
    assert isinstance(fig, matplotlib.figure.Figure), \
        f"Second element should be a Matplotlib Figure, got {type(fig)}"
    assert circ.num_qubits == 3, \
        f"Expected 3 qubits in returned circuit, got {circ.num_qubits}"

    plt.close("all")