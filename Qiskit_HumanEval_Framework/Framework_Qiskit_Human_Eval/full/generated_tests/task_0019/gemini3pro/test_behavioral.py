# BEHAVIORAL tests — Qiskit HumanEval task task_0019
# Generated: 2026-04-28T11:51:49.940826
# Model: google/gemini-3.1-pro-preview (gemini3pro)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    result.remove_final_measurements()\n    backend = FakeTorontoV2()\n    # Check initial layout is not the trivial layout (this is very unlikely\n    # if transpiled with optimization level 3)\n    assert result.layout.initial_index_layout() != list(range(backend.num_qubits))\n    # Optimization level 3 should easily find circuits with depth < 200\n    assert result.depth() < 150\n'
ENTRY_POINT_NAME = 'transpile_circuit_maxopt'
# --- Official check block end ---
def test_transpiled_circuit_properties_1():
    import builtins as _b
    from qiskit import QuantumCircuit
    from qiskit_ibm_runtime.fake_provider import FakeTorontoV2
    
    sol = _b.INJECTED_SOLUTION_CODE
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    transpile_circuit_maxopt = g[_b.INJECTED_ENTRY_POINT]
    
    qc = transpile_circuit_maxopt()
    assert isinstance(qc, QuantumCircuit), "Return type must be a QuantumCircuit."
    
    backend = FakeTorontoV2()
    assert qc.num_qubits == backend.num_qubits or qc.num_qubits == 11, \
        f"Expected {backend.num_qubits} (backend size) or 11 qubits, got {qc.num_qubits}"
    
    basis_gates = set(backend.operation_names)
    basis_gates.update(['measure', 'barrier', 'delay', 'snapshot'])
    
    ops = qc.count_ops()
    assert len(ops) > 0, "Transpiled circuit is empty."
    
    for op in ops:
        assert op in basis_gates, f"Operation '{op}' is not supported by the FakeTorontoV2 basis gates."

def test_ghz_simulation_2():
    import builtins as _b
    from qiskit_aer import AerSimulator
    
    sol = _b.INJECTED_SOLUTION_CODE
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    transpile_circuit_maxopt = g[_b.INJECTED_ENTRY_POINT]
    
    qc = transpile_circuit_maxopt()
    
    # Ensure the circuit has measurements
    if qc.num_clbits == 0:
        qc.measure_all()
        
    # Attempt strict stabilizer simulation, fallback to MPS, then statevector/density matrix
    try:
        sim = AerSimulator(method='stabilizer')
        result = sim.run(qc, shots=2000, seed_simulator=123).result()
    except Exception:
        try:
            sim = AerSimulator(method='matrix_product_state')
            result = sim.run(qc, shots=2000, seed_simulator=123).result()
        except Exception:
            sim = AerSimulator()
            result = sim.run(qc, shots=2000, seed_simulator=123).result()
            
    counts = result.get_counts()
    assert len(counts) > 0, "Simulation yielded no counts."
    
    # An ideal GHZ state yields 2 primary outcomes representing the |0...0> and |1...1> mapped branches
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    assert len(sorted_counts) >= 2, f"Expected at least 2 outcomes for a GHZ state, got {len(sorted_counts)}"
    
    top1_str, top1_cnt = sorted_counts[0]
    top2_str, top2_cnt = sorted_counts[1]
    
    assert top1_cnt + top2_cnt > 1900, "The two most frequent states should dominate the counts (ideal simulation)."
    assert 800 < top1_cnt < 1200, f"Expected ~1000 counts for top state, got {top1_cnt}"
    assert 800 < top2_cnt < 1200, f"Expected ~1000 counts for second state, got {top2_cnt}"
    
    # An 11-qubit GHZ state implies the two superposition branches differ on exactly 11 qubits
    b1 = top1_str.replace(' ', '')
    b2 = top2_str.replace(' ', '')
    diff = sum(c1 != c2 for c1, c2 in zip(b1, b2))
    assert diff == 11, f"Expected Hamming distance of exactly 11 between the two GHZ branches, got {diff}"

def test_optimization_level_3():
    import builtins as _b
    
    sol = _b.INJECTED_SOLUTION_CODE
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    transpile_circuit_maxopt = g[_b.INJECTED_ENTRY_POINT]
    
    qc = transpile_circuit_maxopt()
    
    non_local_count = qc.num_nonlocal_gates()
    
    # An 11-qubit GHZ chain requires at least 10 CNOTs. 
    # Max transpiler optimization on Heavy-Hex will find a line or use minimal swaps.
    # We set an upper bound of 40 to ensure it isn't an unoptimized blob of SWAPs.
    assert non_local_count >= 10, f"An 11-qubit GHZ state requires at least 10 2-qubit gates, got {non_local_count}"
    assert non_local_count <= 40, f"Circuit has {non_local_count} 2-qubit gates; optimization level 3 should yield fewer."