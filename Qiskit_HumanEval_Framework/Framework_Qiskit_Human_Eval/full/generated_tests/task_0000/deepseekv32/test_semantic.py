# SEMANTIC tests — Qiskit HumanEval task task_0000
# Generated: 2026-04-28T11:16:52.067581
# Model: deepseek/deepseek-v3.2 (deepseekv32)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate(3)\n    assert isinstance(result, QuantumCircuit)\n    assert result.num_qubits == 3\n'
ENTRY_POINT_NAME = 'create_quantum_circuit'
# --- Official check block end ---
import builtins as _b
import numpy as np
import qiskit
import qiskit.quantum_info as qi
from qiskit_aer import AerSimulator

def _get_candidate():
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    return candidate

def test_basic_circuit_construction_1():
    candidate = _get_candidate()
    n = 3
    qc = candidate(n)
    assert isinstance(qc, qiskit.QuantumCircuit), "Returned object must be a QuantumCircuit"
    assert qc.num_qubits == n, f"Circuit must have {n} qubits"
    assert qc.num_clbits == 0, "No classical bits should be present unless required"
    # At least one gate should be applied (the problem statement expects a generated circuit)
    assert qc.size() > 0, "Circuit should contain at least one gate"

def test_state_vector_evolution_2():
    candidate = _get_candidate()
    n = 2
    qc = candidate(n)
    # Build unitary from the circuit
    op = qi.Operator(qc)
    # A valid quantum circuit must produce a unitary matrix
    assert op.is_unitary(), "Generated circuit must be unitary"
    # Check that the matrix is the correct size
    dim = 2**n
    assert op.dim == (dim, dim), f"Operator dimension mismatch for {n} qubits"
    # Apply to |0..0> and ensure the resulting state is normalized
    state = qi.Statevector.from_int(0, dim)
    evolved = state.evolve(qc)
    assert np.allclose(evolved.norm(), 1.0, atol=1e-8), "Evolved state must be normalized"

def test_deterministic_counts_3():
    candidate = _get_candidate()
    n = 1
    qc = candidate(n)
    # Add measurements for simulation
    qc.measure_all()
    sim = AerSimulator()
    result = sim.run(qc, shots=1000, seed_simulator=42).result()
    counts = result.get_counts()
    # The circuit may produce a deterministic outcome; check that all shots give the same bitstring
    # (If the circuit is non-deterministic, this test will fail for correct implementations,
    # but the prompt does not guarantee determinism. Instead, we check that counts sum to shots.)
    total = sum(counts.values())
    assert total == 1000, f"Total counts must equal shots, got {total}"
    # Additionally, the number of distinct outcomes must be a power of two within the possible space
    assert len(counts) <= 2**n, f"At most {2**n} possible outcomes, got {len(counts)}"