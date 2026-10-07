# BEHAVIORAL tests — Qiskit HumanEval task task_0020
# Generated: 2026-04-28T11:26:40.536693
# Model: deepseek/deepseek-v3.2 (deepseekv32)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    result.remove_final_measurements()\n    backend = FakePerth()\n    assert result.num_qubits == backend.num_qubits\n    assert result.layout.initial_index_layout()[:3] == [2, 4, 6]\n'
ENTRY_POINT_NAME = 'transpile_ghz_customlayout'
# --- Official check block end ---
def test_returns_circuit_1():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    from qiskit import QuantumCircuit
    
    result = candidate()
    assert isinstance(result, QuantumCircuit), "Function must return a QuantumCircuit instance"
    
    # Check it's not the original trivial circuit (should have been transpiled)
    assert result.num_qubits > 0, "Returned circuit should have qubits"
    assert len(result.data) > 0, "Returned circuit should have gates"

def test_custom_layout_mapping_2():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    from qiskit import QuantumCircuit
    from qiskit_ibm_runtime.fake_provider import FakePerth
    
    result = candidate()
    backend = FakePerth()
    
    # Check that the circuit uses physical qubits from the custom layout [2,4,6]
    # or their mapped equivalents after further swaps
    # At minimum, verify it's been transpiled for Perth backend
    assert result.num_qubits == backend.num_qubits, (
        f"After layout assignment, circuit should have {backend.num_qubits} physical qubits"
    )
    
    # Check that circuit depth > 0 (original GHZ has depth 2: H and 2 CX)
    # After transpilation with layout mapping, depth should be at least original
    assert result.depth() >= 2, "Transpiled circuit should have reasonable depth"
    
    # Verify the circuit can be run on the backend (no invalid operations)
    for instruction, qargs, cargs in result.data:
        for q in qargs:
            assert 0 <= q.index < backend.num_qubits, f"Qubit {q.index} out of range for backend"

def test_ghz_functionality_preserved_3():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator
    import numpy as np
    
    result = candidate()
    
    # Create simulator to test the transpiled circuit still creates GHZ-like entanglement
    # Use a simple simulator without noise to verify logical function
    simulator = AerSimulator()
    
    # Add measurements to all qubits to check outcomes
    measured_circuit = result.copy()
    measured_circuit.measure_all()
    
    # Run simulation
    job = simulator.run(measured_circuit, shots=1024, seed_simulator=42)
    counts = job.result().get_counts()
    
    # For GHZ on 3 logical qubits, we expect |000_ and |111_ on the logical qubits
    # After transpilation with layout [2,4,6], the physical qubits 2,4,6 should be entangled
    # Check that we get only two bitstrings (all 0 or all 1) on SOME subset of qubits
    # Not checking exact positions because layout+swap may change mapping
    
    # More robust: check that there are exactly 2 outcomes (up to measurement noise)
    # This indicates entanglement between some set of qubits
    num_outcomes = len(counts)
    assert num_outcomes == 2, (
        f"GHZ circuit should produce 2 outcomes, got {num_outcomes}: {counts}"
    )
    
    # The two outcomes should be complementary (all 0s and all 1s on the same qubits)
    outcomes = list(counts.keys())
    if len(outcomes) == 2:
        # Convert to strings if needed
        str1, str2 = outcomes[0], outcomes[1]
        # Check they are bitwise complements on the participating qubits
        # Find positions where they differ
        diff_positions = [i for i in range(len(str1)) if str1[i] != str2[i]]
        # All differing positions should flip together (GHZ property)
        # This means for any two differing positions i,j: str1[i]==str1[j] and str2[i]==str2[j]
        if diff_positions:
            first_diff = diff_positions[0]
            for pos in diff_positions:
                assert str1[pos] == str1[first_diff], "Not all entangled qubits have same value in |000_ state"
                assert str2[pos] == str2[first_diff], "Not all entangled qubits have same value in |111_ state"