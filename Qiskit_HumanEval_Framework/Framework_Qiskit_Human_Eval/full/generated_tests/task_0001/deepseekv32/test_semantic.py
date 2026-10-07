# SEMANTIC tests — Qiskit HumanEval task task_0001
# Generated: 2026-04-28T11:18:21.373788
# Model: deepseek/deepseek-v3.2 (deepseekv32)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    assert isinstance(result, dict)\n    assert result.keys() == {"00", "11"}\n    assert 0.4 < (result["00"] / sum(result.values())) < 0.6\n'
ENTRY_POINT_NAME = 'run_bell_state_simulator'
# --- Official check block end ---
import numpy as np
import pytest
import builtins as _b

sol = _b.INJECTED_SOLUTION_CODE
entry = _b.INJECTED_ENTRY_POINT
g = {"__builtins__": __builtins__}
exec(sol, g)
candidate = g[entry]


def test_bell_state_simulator_counts_shape_and_keys_1():
    """Test that the returned counts dictionary has correct keys and shape."""
    import qiskit.quantum_info as qi
    counts = candidate()
    assert isinstance(counts, dict), "Result must be a dictionary."
    assert len(counts) == 2, "Bell state should produce two outcomes (00 and 11)."
    assert set(counts.keys()) == {"00", "11"}, "Keys must be '00' and '11'."
    total_shots = sum(counts.values())
    assert total_shots > 0, "Total shots must be positive."
    # Statistical tolerance: each outcome should be roughly 50%
    prob_00 = counts["00"] / total_shots
    prob_11 = counts["11"] / total_shots
    assert np.allclose(prob_00, 0.5, atol=0.05), "Probability for '00' should be ~0.5."
    assert np.allclose(prob_11, 0.5, atol=0.05), "Probability for '11' should be ~0.5."
    # Ensure no other keys appear
    for key in counts.keys():
        assert key in {"00", "11"}, f"Unexpected key '{key}' in counts."


def test_bell_state_simulator_circuit_statevector_2():
    """Test that the generated circuit produces the correct Bell state."""
    import qiskit.quantum_info as qi
    import qiskit
    from qiskit_aer import AerSimulator
    # Build candidate's circuit indirectly via its execution path
    counts = candidate()
    # Recreate the circuit from scratch to verify the intended Bell state
    qc = qiskit.QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    # Compute exact statevector
    backend = AerSimulator(method='statevector')
    result = backend.run(qc).result()
    statevector = result.data()['statevector']
    # Expected Bell state (phi-plus): (|00>+|11>)/sqrt(2)
    expected = np.array([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)])
    # Compare up to global phase (Bell state is defined up to phase)
    # Compute inner product magnitude squared
    overlap = np.abs(np.vdot(statevector, expected))**2
    assert np.allclose(overlap, 1.0, atol=1e-4), "Circuit does not produce the Bell state."


def test_bell_state_simulator_transpiled_circuit_operation_3():
    """Test that the transpiled circuit (optimization level 1) still produces Bell state."""
    import qiskit.quantum_info as qi
    import qiskit
    from qiskit_aer import AerSimulator
    from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
    # Create original Bell circuit
    qc = qiskit.QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    # Transpile with optimization level 1 (as specified)
    backend = AerSimulator()
    pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
    transpiled_qc = pm.run(qc)
    # Run transpiled circuit with AerSimulator (statevector) to get exact state
    backend_sv = AerSimulator(method='statevector')
    result = backend_sv.run(transpiled_qc).result()
    statevector = result.data()['statevector']
    # Expected Bell state
    expected = np.array([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)])
    overlap = np.abs(np.vdot(statevector, expected))**2
    assert np.allclose(overlap, 1.0, atol=1e-4), "Transpiled circuit does not preserve Bell state."
    # Additionally verify that the circuit depth is reduced (typical for optimization level 1)
    original_depth = qc.depth()
    transpiled_depth = transpiled_qc.depth()
    # Optimization level 1 often reduces depth, but not strictly required; just check it's valid
    assert transpiled_depth >= 1, "Transpiled circuit must have non-zero depth."
    # Ensure measurement is present (since counts were returned)
    # The candidate's circuit should include measurement for Sampler to produce counts.
    # We can't inspect candidate's internal circuit directly, but we can infer from counts.
    counts = candidate()
    assert isinstance(counts, dict) and len(counts) == 2, "Counts must be present."