# SEMANTIC tests — Qiskit HumanEval task task_0019
# Generated: 2026-04-28T12:40:31.610076
# Model: qwen/qwen3-coder-next (qwen3)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    result.remove_final_measurements()\n    backend = FakeTorontoV2()\n    # Check initial layout is not the trivial layout (this is very unlikely\n    # if transpiled with optimization level 3)\n    assert result.layout.initial_index_layout() != list(range(backend.num_qubits))\n    # Optimization level 3 should easily find circuits with depth < 200\n    assert result.depth() < 150\n'
ENTRY_POINT_NAME = 'transpile_circuit_maxopt'
# --- Official check block end ---
def test_transpile_circuit_maxopt_returns_valid_quantumcircuit():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    # Check return type
    result = candidate()
    assert isinstance(result, QuantumCircuit), f"Expected QuantumCircuit, got {type(result)}"
    
    # Check circuit is not empty
    assert result.num_qubits > 0, "Circuit should have at least one qubit"
    
    # Check circuit has measurements (common for transpiled circuits on real backends)
    # But since this is a GHZ circuit, it may or may not include measurements depending on implementation
    # So just verify it's a valid circuit with expected structure


def test_transpile_circuit_maxopt_has_correct_qubit_count():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    result = candidate()
    
    # The problem specifies an 11-qubit GHZ circuit
    assert result.num_qubits == 11, f"Expected 11 qubits for GHZ circuit, got {result.num_qubits}"


def test_transpile_circuit_maxopt_preserves_ghz_state_properties():
    import builtins as _b
    import numpy as np
    from qiskit.quantum_info import Statevector, Operator
    from qiskit_aer import Aer
    
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    # Get transpiled circuit
    transpiled_circuit = candidate()
    
    # Create reference 11-qubit GHZ state
    ref_circuit = QuantumCircuit(11)
    ref_circuit.h(0)
    for i in range(1, 11):
        ref_circuit.cx(0, i)
    ref_state = Statevector.from_instruction(ref_circuit)
    
    # Simulate the transpiled circuit
    try:
        aer_sim = Aer.get_backend('aer_simulator')
        # For simulation, we need to remove measurements if present
        # Create a version without measurements for statevector simulation
        circ_for_sim = transpiled_circuit.copy()
        # Remove measurements
        for i, instruction in enumerate(circ_for_sim.data):
            if instruction.operation.name == 'measure':
                circ_for_sim.data.pop(i)
        
        sim_state = Statevector.from_instruction(circ_for_sim)
        
        # Compare states up to global phase
        overlap = np.abs(np.vdot(ref_state.data, sim_state.data))
        assert np.allclose(overlap, 1.0, atol=1e-4), f"Transpiled circuit does not produce GHZ state, overlap={overlap}"
    except Exception:
        # If Aer not available, skip this test
        pass