# SEMANTIC tests — Qiskit HumanEval task task_0019
# Generated: 2026-04-28T11:24:05.342293
# Model: deepseek/deepseek-v3.2 (deepseekv32)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    result.remove_final_measurements()\n    backend = FakeTorontoV2()\n    # Check initial layout is not the trivial layout (this is very unlikely\n    # if transpiled with optimization level 3)\n    assert result.layout.initial_index_layout() != list(range(backend.num_qubits))\n    # Optimization level 3 should easily find circuits with depth < 200\n    assert result.depth() < 150\n'
ENTRY_POINT_NAME = 'transpile_circuit_maxopt'
# --- Official check block end ---
import builtins as _b
import pytest
import numpy as np
from qiskit import QuantumCircuit
from qiskit_ibm_runtime.fake_provider import FakeTorontoV2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

sol = _b.INJECTED_SOLUTION_CODE
entry = _b.INJECTED_ENTRY_POINT
g = {"__builtins__": __builtins__}
exec(sol, g)
transpile_circuit_maxopt = g[entry]

def test_returns_circuit_instance_1():
    """Check that the function returns a QuantumCircuit instance."""
    result = transpile_circuit_maxopt()
    assert isinstance(result, QuantumCircuit), f"Expected QuantumCircuit, got {type(result)}"

def test_circuit_uses_fake_toronto_v2_connectivity_2():
    """Verify the transpiled circuit respects the FakeTorontoV2 coupling map."""
    from qiskit_ibm_runtime.fake_provider import FakeTorontoV2
    from qiskit.transpiler import CouplingMap

    backend = FakeTorontoV2()
    coupling_map = CouplingMap(backend.coupling_map)

    result = transpile_circuit_maxopt()
    # Check that every two-qubit gate uses a coupled pair.
    for instr in result.data:
        if len(instr.qubits) == 2:
            q0 = result.find_bit(instr.qubits[0]).index
            q1 = result.find_bit(instr.qubits[1]).index
            assert coupling_map.graph.has_edge(q0, q1), f"Two-qubit gate on uncoupled qubits ({q0}, {q1})"

def test_transpiled_circuit_preserves_ghz_state_3():
    """Check that the transpiled circuit still prepares an 11-qubit GHZ state up to global phase."""
    from qiskit.quantum_info import Statevector
    from qiskit_aer import AerSimulator

    # Original GHZ on 11 qubits.
    qc = QuantumCircuit(11)
    qc.h(0)
    for i in range(10):
        qc.cx(i, i+1)
    # Simulate the original.
    sim = AerSimulator()
    original_counts = sim.run(qc, shots=1000, seed_simulator=42).result().get_counts()

    # Get transpiled circuit from candidate.
    transpiled = transpile_circuit_maxopt()
    # Ensure it has 11 qubits.
    assert transpiled.num_qubits == 11, f"Expected 11 qubits, got {transpiled.num_qubits}"
    # Simulate the transpiled.
    transpiled_counts = sim.run(transpiled, shots=1000, seed_simulator=42).result().get_counts()

    # GHZ states produce only two outcomes: all-zeros and all-ones.
    # Build expected keys.
    expected_keys = {'0'*11, '1'*11}
    # Check that all observed keys are among expected.
    for key in original_counts.keys():
        assert key in expected_keys, f"Original circuit produced unexpected outcome {key}"
    for key in transpiled_counts.keys():
        assert key in expected_keys, f"Transpiled circuit produced unexpected outcome {key}"
    # Since the transpilation may add ancillas_ No, we have 11 qubits, so just compare that
    # both circuits give the same distribution shape.
    # We'll check that the two outcomes dominate.
    total_original = sum(original_counts.values())
    total_transpiled = sum(transpiled_counts.values())
    # Sum of probabilities for the two GHZ outcomes should be near 1.
    prob_original = sum(original_counts.get(k, 0) for k in expected_keys) / total_original
    prob_transpiled = sum(transpiled_counts.get(k, 0) for k in expected_keys) / total_transpiled
    assert np.allclose(prob_original, 1.0, atol=0.05), f"Original circuit not GHZ, probability {prob_original}"
    assert np.allclose(prob_transpiled, 1.0, atol=0.05), f"Transpiled circuit not GHZ, probability {prob_transpiled}"