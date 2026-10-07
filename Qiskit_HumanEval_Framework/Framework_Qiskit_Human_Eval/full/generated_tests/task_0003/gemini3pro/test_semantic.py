# SEMANTIC tests — Qiskit HumanEval task task_0003
# Generated: 2026-04-28T11:46:29.982219
# Model: google/gemini-3.1-pro-preview (gemini3pro)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from qiskit.quantum_info import Statevector\n    import math\n    import matplotlib\n\n    def check_circuit(circuit):\n        assert circuit.data[-1].operation.name == "measure"\n        circuit.remove_final_measurements()\n        ghz_statevector = (\n            Statevector.from_label("000") + Statevector.from_label("111")\n        ) / math.sqrt(2)\n        assert Statevector.from_instruction(circuit).equiv(ghz_statevector)\n\n    circuit = candidate()\n    check_circuit(circuit)\n\n    circuit, drawing = candidate(drawing=True)\n    check_circuit(circuit)\n    assert isinstance(drawing, matplotlib.figure.Figure)\n'
ENTRY_POINT_NAME = 'create_ghz'
# --- Official check block end ---
def test_create_ghz_1():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator
    
    # Test default behavior (drawing=False)
    qc = candidate(drawing=False)
    assert isinstance(qc, QuantumCircuit), "Expected a QuantumCircuit object to be returned."
    assert qc.num_qubits == 3, f"Expected exactly 3 qubits, got {qc.num_qubits}."
    
    has_measure = any(inst.operation.name == 'measure' for inst in qc.data)
    assert has_measure, "Circuit must include measurements as requested by the prompt."
    
    sim = AerSimulator()
    res = sim.run(qc, shots=2000, seed_simulator=123).result()
    counts = res.get_counts()
    
    assert len(counts) > 0, "No counts returned from the circuit measurement."
    
    for k, v in counts.items():
        k_clean = k.replace(' ', '')
        num_ones = k_clean.count('1')
        # A valid GHZ state measurement yields either all 0s or all 1s for the measured qubits.
        assert num_ones == 3 or num_ones == 0, f"Found unexpected state '{k}' in counts. A 3-qubit GHZ state should yield all 0s or all 1s."
        assert v > 800, f"Counts for state '{k}' are too low ({v} out of 2000). Should be roughly 1000."
        
    has_zeros = any(k.replace(' ', '').count('1') == 0 for k in counts.keys())
    has_ones = any(k.replace(' ', '').count('1') == 3 for k in counts.keys())
    assert has_zeros and has_ones, "Measurement results must include both all-0 and all-1 outcomes."

def test_create_ghz_2():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    from qiskit import QuantumCircuit
    
    # Test drawing behavior (drawing=True)
    result = candidate(drawing=True)
    assert isinstance(result, tuple), "Expected a tuple to be returned when drawing=True."
    assert len(result) == 2, f"Expected tuple of length 2, got {len(result)}."
    
    qc, fig = result
    assert isinstance(qc, QuantumCircuit), "First element of the tuple must be a QuantumCircuit."
    
    fig_class_name = type(fig).__name__
    assert fig_class_name == 'Figure', f"Expected the second element to be a Matplotlib Figure, got {fig_class_name}."

def test_create_ghz_3():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    import numpy as np
    from qiskit.quantum_info import Statevector
    from qiskit import QuantumCircuit

    # Test the underlying pure state vector before measurement
    qc = candidate(drawing=False)
    
    qc_unmeasured = QuantumCircuit(qc.num_qubits)
    for inst in qc.data:
        # Strip measurements, barriers, and any classical conditioning to extract pure state preparation
        if inst.operation.name not in ['measure', 'barrier'] and not inst.clbits:
            qargs = [qc.qubits.index(q) for q in inst.qubits]
            qc_unmeasured.append(inst.operation, qargs)
            
    sv = Statevector.from_instruction(qc_unmeasured)
    probs = np.abs(sv.data)**2
    
    assert np.isclose(probs[0], 0.5, atol=1e-4), f"Probability of |000> should be 0.5, got {probs[0]}"
    assert np.isclose(probs[7], 0.5, atol=1e-4), f"Probability of |111> should be 0.5, got {probs[7]}"
    assert np.isclose(np.sum(probs[[0, 7]]), 1.0, atol=1e-4), "State must only contain |000> and |111> components."