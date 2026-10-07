# SEMANTIC tests — Qiskit HumanEval task task_0003
# Generated: 2026-04-28T11:10:42.514069
# Model: anthropic/claude-opus-4-6 (claudeopus46)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from qiskit.quantum_info import Statevector\n    import math\n    import matplotlib\n\n    def check_circuit(circuit):\n        assert circuit.data[-1].operation.name == "measure"\n        circuit.remove_final_measurements()\n        ghz_statevector = (\n            Statevector.from_label("000") + Statevector.from_label("111")\n        ) / math.sqrt(2)\n        assert Statevector.from_instruction(circuit).equiv(ghz_statevector)\n\n    circuit = candidate()\n    check_circuit(circuit)\n\n    circuit, drawing = candidate(drawing=True)\n    check_circuit(circuit)\n    assert isinstance(drawing, matplotlib.figure.Figure)\n'
ENTRY_POINT_NAME = 'create_ghz'
# --- Official check block end ---
import pytest

def test_ghz_circuit_structure_1():
    """Test that the returned circuit has correct number of qubits, classical bits, and measurements."""
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    qc = candidate(drawing=False)

    from qiskit import QuantumCircuit
    assert isinstance(qc, QuantumCircuit), "Return value should be a QuantumCircuit when drawing=False"
    assert qc.num_qubits == 3, f"Expected 3 qubits, got {qc.num_qubits}"
    assert qc.num_clbits == 3, f"Expected 3 classical bits for measurement, got {qc.num_clbits}"

    # Check that measurements are present
    op_names = [inst.operation.name for inst in qc.data]
    measure_count = op_names.count('measure')
    assert measure_count == 3, f"Expected 3 measure operations, got {measure_count}"


def test_ghz_statevector_2():
    """Test that the circuit (without measurements) produces the correct GHZ state |000> + |111> / sqrt(2)."""
    import builtins as _b
    import numpy as np
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    qc = candidate(drawing=False)

    # Remove measurements to get the statevector
    from qiskit import QuantumCircuit
    qc_no_meas = qc.remove_final_measurements(inplace=False)

    from qiskit.quantum_info import Statevector
    sv = Statevector.from_instruction(qc_no_meas)
    probs = sv.probabilities()

    # GHZ state: equal superposition of |000> and |111>
    # In Qiskit's ordering, |000> is index 0 and |111> is index 7
    assert np.isclose(probs[0], 0.5, atol=1e-4), f"Probability of |000> should be 0.5, got {probs[0]}"
    assert np.isclose(probs[7], 0.5, atol=1e-4), f"Probability of |111> should be 0.5, got {probs[7]}"

    # All other probabilities should be zero
    for i in range(8):
        if i not in (0, 7):
            assert np.isclose(probs[i], 0.0, atol=1e-4), f"Probability of state |{i:03b}> should be 0, got {probs[i]}"


def test_ghz_drawing_return_3():
    """Test that when drawing=True, the function returns a tuple of (circuit, figure)."""
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    import matplotlib
    matplotlib.use('Agg')  # non-interactive backend

    result = candidate(drawing=True)

    assert isinstance(result, (tuple, list)), \
        f"When drawing=True, should return a tuple/list, got {type(result)}"
    assert len(result) == 2, f"Expected 2 elements (circuit, figure), got {len(result)}"

    from qiskit import QuantumCircuit
    import matplotlib.figure
    assert isinstance(result[0], QuantumCircuit), \
        f"First element should be a QuantumCircuit, got {type(result[0])}"
    assert isinstance(result[1], matplotlib.figure.Figure), \
        f"Second element should be a matplotlib Figure, got {type(result[1])}"