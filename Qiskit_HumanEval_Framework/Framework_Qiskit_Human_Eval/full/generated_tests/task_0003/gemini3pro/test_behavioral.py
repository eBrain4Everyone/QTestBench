# BEHAVIORAL tests — Qiskit HumanEval task task_0003
# Generated: 2026-04-28T11:47:37.123532
# Model: google/gemini-3.1-pro-preview (gemini3pro)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from qiskit.quantum_info import Statevector\n    import math\n    import matplotlib\n\n    def check_circuit(circuit):\n        assert circuit.data[-1].operation.name == "measure"\n        circuit.remove_final_measurements()\n        ghz_statevector = (\n            Statevector.from_label("000") + Statevector.from_label("111")\n        ) / math.sqrt(2)\n        assert Statevector.from_instruction(circuit).equiv(ghz_statevector)\n\n    circuit = candidate()\n    check_circuit(circuit)\n\n    circuit, drawing = candidate(drawing=True)\n    check_circuit(circuit)\n    assert isinstance(drawing, matplotlib.figure.Figure)\n'
ENTRY_POINT_NAME = 'create_ghz'
# --- Official check block end ---
def test_create_ghz_1():
    import builtins as _b
    from qiskit import QuantumCircuit
    
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    qc = candidate(drawing=False)
    
    assert isinstance(qc, QuantumCircuit), "Return type must be a QuantumCircuit when drawing=False."
    assert qc.num_qubits == 3, f"Expected 3 qubits, found {qc.num_qubits}."
    assert qc.num_clbits >= 3, f"Expected at least 3 classical bits, found {qc.num_clbits}."
    
    has_measure = any(instr.operation.name == "measure" for instr in qc.data)
    assert has_measure, "Circuit must contain measurement operations."


def test_create_ghz_2():
    import builtins as _b
    from qiskit import QuantumCircuit
    
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    result = candidate(drawing=True)
    
    assert isinstance(result, tuple), "Expected a tuple when drawing=True."
    assert len(result) == 2, f"Expected tuple of length 2, got {len(result)}."
    
    qc, fig = result
    assert isinstance(qc, QuantumCircuit), "First element of tuple must be a QuantumCircuit."
    assert "Figure" in type(fig).__name__, "Second element of tuple must be a matplotlib Figure."


def test_create_ghz_3():
    import builtins as _b
    import numpy as np
    from qiskit import transpile
    from qiskit_aer import AerSimulator
    
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    qc = candidate(drawing=False)
    
    sim = AerSimulator()
    qc_t = transpile(qc, sim)
    res = sim.run(qc_t, shots=2048, seed_simulator=123).result()
    counts = res.get_counts()
    
    counts_clean = {k.replace(' ', ''): v for k, v in counts.items()}
    
    assert len(counts_clean) == 2, f"Expected exactly 2 distinct outcomes for GHZ state, got {len(counts_clean)}: {counts_clean}"
    
    keys = list(counts_clean.keys())
    diff = sum(1 for a, b in zip(keys[0], keys[1]) if a != b)
    assert diff == 3, f"Expected exactly 3 bits to differ between the two outcomes, found {diff}. Outcomes: {keys}"
    
    total_shots = sum(counts_clean.values())
    for k in keys:
        p = counts_clean[k] / total_shots
        assert np.isclose(p, 0.5, atol=0.05), f"Outcome probability for {k} should be ~0.5, but got {p:.3f}"