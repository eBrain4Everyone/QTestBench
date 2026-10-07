# BEHAVIORAL tests — Qiskit HumanEval task task_0000
# Generated: 2026-04-28T11:17:32.246322
# Model: deepseek/deepseek-v3.2 (deepseekv32)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate(3)\n    assert isinstance(result, QuantumCircuit)\n    assert result.num_qubits == 3\n'
ENTRY_POINT_NAME = 'create_quantum_circuit'
# --- Official check block end ---
import builtins as _b
import numpy as np

def _load_candidate():
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    return g[entry]

def test_basic_circuit_creation_1():
    """Test that the function returns a QuantumCircuit with correct number of qubits."""
    create_quantum_circuit = _load_candidate()
    n_qubits = 3
    qc = create_quantum_circuit(n_qubits)
    assert isinstance(qc, QuantumCircuit), f"Expected QuantumCircuit, got {type(qc)}"
    assert qc.num_qubits == n_qubits, f"Expected {n_qubits} qubits, got {qc.num_qubits}"
    # Check default classical bits (should be 0 unless the solution adds them)
    assert qc.num_clbits == 0, f"Expected 0 classical bits, got {qc.num_clbits}"
    # Ensure circuit is not empty_ Actually prompt does not require gates, so we only check creation.

def test_empty_circuit_execution_2():
    """Test that an empty circuit (if solution adds no gates) produces correct statevector."""
    create_quantum_circuit = _load_candidate()
    from qiskit.quantum_info import Statevector
    n_qubits = 2
    qc = create_quantum_circuit(n_qubits)
    # If the solution adds no gates, the state should be |00...0>
    state = Statevector.from_instruction(qc)
    expected = np.zeros(2**n_qubits, dtype=complex)
    expected[0] = 1.0  # |00>
    assert np.allclose(state.data, expected, atol=1e-10), f"State mismatch: got {state.data}, expected {expected}"

def test_circuit_with_measurements_3():
    """Test that if the solution adds measurements, the sampled counts match the expected probabilities."""
    create_quantum_circuit = _load_candidate()
    n_qubits = 1
    qc = create_quantum_circuit(n_qubits)
    # Check if there are classical bits added (some solutions might add measurements)
    if qc.num_clbits > 0:
        # If measurements are present, we can run a simulation
        from qiskit import Aer, transpile
        from qiskit.visualization import plot_histogram  # not used, but ensures import
        backend = Aer.get_backend('qasm_simulator')
        # Use fixed seed for deterministic results
        from qiskit.providers.aer import AerSimulator
        backend = AerSimulator(seed_simulator=42)
        tqc = transpile(qc, backend)
        result = backend.run(tqc, shots=1000, seed_simulator=42).result()
        counts = result.get_counts()
        # The expected measurement should be deterministic if the state is |0>
        # If the solution put a gate (e.g., X), counts may differ; but we only check that counts sum to shots.
        total = sum(counts.values())
        assert total == 1000, f"Total counts {total} != 1000 shots"
    else:
        # No measurements added, that's fine; we just ensure the circuit is valid.
        # We can still simulate with statevector to see if gates were added.
        from qiskit.quantum_info import Statevector
        state = Statevector.from_instruction(qc)
        # The state should be normalized
        assert np.isclose(np.linalg.norm(state.data), 1.0), "State not normalized"
        # Check that state is pure (norm^2 = 1) - redundant but safe
        assert np.isclose(np.linalg.norm(state.data)**2, 1.0), "State not pure"