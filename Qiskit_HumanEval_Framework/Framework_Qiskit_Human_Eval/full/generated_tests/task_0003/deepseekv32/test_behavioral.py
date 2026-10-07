# BEHAVIORAL tests — Qiskit HumanEval task task_0003
# Generated: 2026-04-28T11:23:03.096972
# Model: deepseek/deepseek-v3.2 (deepseekv32)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from qiskit.quantum_info import Statevector\n    import math\n    import matplotlib\n\n    def check_circuit(circuit):\n        assert circuit.data[-1].operation.name == "measure"\n        circuit.remove_final_measurements()\n        ghz_statevector = (\n            Statevector.from_label("000") + Statevector.from_label("111")\n        ) / math.sqrt(2)\n        assert Statevector.from_instruction(circuit).equiv(ghz_statevector)\n\n    circuit = candidate()\n    check_circuit(circuit)\n\n    circuit, drawing = candidate(drawing=True)\n    check_circuit(circuit)\n    assert isinstance(drawing, matplotlib.figure.Figure)\n'
ENTRY_POINT_NAME = 'create_ghz'
# --- Official check block end ---
import builtins as _b

def test_basic_circuit_1():
    import qiskit
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    # Test with drawing=False (default)
    result = candidate(drawing=False)
    assert isinstance(result, qiskit.QuantumCircuit), f"Expected QuantumCircuit, got {type(result)}"
    # Check it's a 3_qubit circuit with measurements
    assert result.num_qubits == 3, f"Expected 3 qubits, got {result.num_qubits}"
    assert result.num_clbits == 3, f"Expected 3 classical bits, got {result.num_clbits}"
    # Check the gates: H on qubit 0, CNOTs 0_1 and 0_2, then measurements
    # We'll check the count of each operation roughly
    ops = result.count_ops()
    assert ops.get('h', 0) == 1, f"Expected exactly one H gate, got {ops.get('h', 0)}"
    assert ops.get('cx', 0) == 2, f"Expected exactly two CX gates, got {ops.get('cx', 0)}"
    # At least three measurements (maybe more if user adds extra)
    assert ops.get('measure', 0) >= 3, f"Expected at least three measurements, got {ops.get('measure', 0)}"

def test_drawing_true_2():
    import qiskit
    import matplotlib.pyplot as plt
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    result = candidate(drawing=True)
    assert isinstance(result, tuple), f"Expected a tuple when drawing=True, got {type(result)}"
    assert len(result) == 2, f"Expected tuple of length 2, got {len(result)}"
    qc, drawing = result
    assert isinstance(qc, qiskit.QuantumCircuit), f"First element should be QuantumCircuit, got {type(qc)}"
    # The drawing is a matplotlib.axes.AxesSubplot (or similar) when circuit.draw() is called with matplotlib backend.
    # Check it's a matplotlib.axes.Axes (or at least has typical methods).
    assert hasattr(drawing, 'figure'), f"Drawing should have a 'figure' attribute (matplotlib Axes), got {type(drawing)}"
    # Quick sanity: circuit should be the same as in test_1
    assert qc.num_qubits == 3, f"Circuit should have 3 qubits, got {qc.num_qubits}"
    assert qc.num_clbits == 3, f"Circuit should have 3 classical bits, got {qc.num_clbits}"
    ops = qc.count_ops()
    assert ops.get('h', 0) == 1, f"Expected one H gate, got {ops.get('h', 0)}"
    assert ops.get('cx', 0) == 2, f"Expected two CX gates, got {ops.get('cx', 0)}"

def test_ghz_counts_3():
    import qiskit
    import numpy as np
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    qc = candidate(drawing=False)
    # Ensure it's a GHZ circuit (3 qubits) and has measurements.
    # Run simulation with a fixed seed.
    from qiskit_aer import AerSimulator
    backend = AerSimulator(seed_simulator=42)
    # Transpile for backend (optional, but safe)
    from qiskit import transpile
    tqc = transpile(qc, backend)
    result = backend.run(tqc, shots=1024, seed_simulator=42).result()
    counts = result.get_counts()
    # GHZ state is |000> + |111> (up to normalization)
    # So only two outcomes should appear
    expected_keys = {'000', '111'}
    assert set(counts.keys()) == expected_keys, f"Expected only '000' and '111', got {set(counts.keys())}"
    # Check rough 50/50 distribution (allow 5% tolerance)
    total = sum(counts.values())
    prob0 = counts.get('000', 0) / total
    prob1 = counts.get('111', 0) / total
    assert np.isclose(prob0, 0.5, atol=0.05), f"Probability of '000' should be ~0.5, got {prob0}"
    assert np.isclose(prob1, 0.5, atol=0.05), f"Probability of '111' should be ~0.5, got {prob1}"