# SEMANTIC tests — Qiskit HumanEval task task_0020
# Generated: 2026-04-28T11:53:52.910930
# Model: google/gemini-3.1-pro-preview (gemini3pro)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    result.remove_final_measurements()\n    backend = FakePerth()\n    assert result.num_qubits == backend.num_qubits\n    assert result.layout.initial_index_layout()[:3] == [2, 4, 6]\n'
ENTRY_POINT_NAME = 'transpile_ghz_customlayout'
# --- Official check block end ---
def test_transpile_ghz_customlayout_1():
    import builtins as _b
    from qiskit import QuantumCircuit
    
    g = {"__builtins__": __builtins__}
    exec(_b.INJECTED_SOLUTION_CODE, g)
    transpile_ghz_customlayout = g[_b.INJECTED_ENTRY_POINT]
    
    qc = transpile_ghz_customlayout()
    assert isinstance(qc, QuantumCircuit), "Return type must be a QuantumCircuit."
    assert qc.num_qubits == 7, f"FakePerth has 7 qubits, but the returned circuit has {qc.num_qubits} qubits."
    assert len(qc.data) > 0, "The returned transpiled circuit should not be empty."

def test_transpile_ghz_customlayout_2():
    import builtins as _b
    
    g = {"__builtins__": __builtins__}
    exec(_b.INJECTED_SOLUTION_CODE, g)
    transpile_ghz_customlayout = g[_b.INJECTED_ENTRY_POINT]
    
    qc = transpile_ghz_customlayout()
    
    assert hasattr(qc, '_layout') and qc._layout is not None, "Transpiled circuit must have a _layout attribute populated."
    
    initial_layout = qc._layout.initial_layout
    assert initial_layout is not None, "The initial_layout of the transpiled circuit cannot be None."
    
    physical_bits = initial_layout.get_virtual_bits()
    
    # Filter out ancilla qubits added by the transpiler to find where logical qubits were mapped
    non_ancilla_phys = []
    for v_qubit, p_idx in physical_bits.items():
        reg_name = v_qubit.register.name if v_qubit.register is not None else ""
        if reg_name != 'ancilla':
            non_ancilla_phys.append(p_idx)
            
    expected_layout = [2, 4, 6]
    assert sorted(non_ancilla_phys) == expected_layout, \
        f"Expected logical qubits to be mapped exactly to physical qubits {expected_layout}, got {sorted(non_ancilla_phys)}."

def test_transpile_ghz_customlayout_3():
    import builtins as _b
    import numpy as np
    from qiskit.quantum_info import Statevector
    from qiskit import QuantumCircuit
    
    g = {"__builtins__": __builtins__}
    exec(_b.INJECTED_SOLUTION_CODE, g)
    transpile_ghz_customlayout = g[_b.INJECTED_ENTRY_POINT]
    
    qc = transpile_ghz_customlayout()
    
    # Remove measurements and barriers to allow exact Statevector simulation
    qc_no_meas = QuantumCircuit(*qc.qregs, *qc.cregs)
    for inst in qc.data:
        if inst.operation.name not in ['measure', 'barrier']:
            qc_no_meas.append(inst)
            
    sv = Statevector.from_instruction(qc_no_meas)
    probs = sv.probabilities()
    
    # Retrieve computational basis states with a non-zero probability
    non_zero_indices = np.where(probs > 1e-3)[0]
    assert len(non_zero_indices) == 2, \
        f"A valid GHZ state mapped to a larger backend should have exactly 2 basis states with non-zero probability. Found {len(non_zero_indices)}."
    
    for idx in non_zero_indices:
        assert np.isclose(probs[idx], 0.5, atol=1e-2), \
            f"Expected probability of each branch to be ~0.5, but state {idx} has probability {probs[idx]}."
        
    idx1, idx2 = non_zero_indices
    bin1 = format(idx1, f'0{qc.num_qubits}b')
    bin2 = format(idx2, f'0{qc.num_qubits}b')
    
    # The two basis states of the GHZ superposition should differ in exactly 3 bit positions 
    # (the 3 logical qubits, regardless of their final physical routing)
    diff_bits = sum(1 for b1, b2 in zip(bin1, bin2) if b1 != b2)
    assert diff_bits == 3, \
        f"The two basis states should differ in exactly 3 bits for a 3-qubit GHZ state padded with ancillas, but they differ by {diff_bits}. States: {bin1}, {bin2}."