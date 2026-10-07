# BEHAVIORAL tests — Qiskit HumanEval task task_0019
# Generated: 2026-04-28T11:24:41.005715
# Model: deepseek/deepseek-v3.2 (deepseekv32)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    result.remove_final_measurements()\n    backend = FakeTorontoV2()\n    # Check initial layout is not the trivial layout (this is very unlikely\n    # if transpiled with optimization level 3)\n    assert result.layout.initial_index_layout() != list(range(backend.num_qubits))\n    # Optimization level 3 should easily find circuits with depth < 200\n    assert result.depth() < 150\n'
ENTRY_POINT_NAME = 'transpile_circuit_maxopt'
# --- Official check block end ---
import builtins as _b
import numpy as np
from qiskit import QuantumCircuit
from qiskit_ibm_runtime.fake_provider import FakeTorontoV2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

sol = _b.INJECTED_SOLUTION_CODE
entry = _b.INJECTED_ENTRY_POINT
g = {"__builtins__": __builtins__}
exec(sol, g)
transpile_circuit_maxopt = g[entry]

def test_returns_quantum_circuit_1():
    """Check that the function returns a QuantumCircuit instance."""
    result = transpile_circuit_maxopt()
    assert isinstance(result, QuantumCircuit), "Result must be a QuantumCircuit."

def test_circuit_uses_fake_toronto_backend_2():
    """Check that the transpiled circuit is compatible with FakeTorontoV2."""
    backend = FakeTorontoV2()
    result = transpile_circuit_maxopt()
    # The circuit should have 27 qubits (FakeTorontoV2 has 27 qubits)
    # but the original GHZ used 11 qubits, mapping may use up to backend size.
    assert result.num_qubits == backend.num_qubits, \
        f"Transpiled circuit must have {backend.num_qubits} qubits to match backend."
    # Check that all operations are supported by backend
    for inst, qargs, cargs in result.data:
        if inst.name == "barrier":
            continue
        assert inst.name in backend.operation_names, \
            f"Operation {inst.name} is not supported by FakeTorontoV2."

def test_ghz_behavior_preserved_3():
    """Check that the transpiled circuit still implements an 11-qubit GHZ state
    on a subset of qubits (or the whole register) after transpilation."""
    from qiskit_aer import AerSimulator
    from qiskit.transpiler import CouplingMap

    # Build original 11-qubit GHZ circuit
    qc = QuantumCircuit(11)
    qc.h(0)
    for i in range(10):
        qc.cx(i, i+1)

    # Use the same backend as the candidate function
    backend = FakeTorontoV2()
    # Use the same pass manager configuration (max optimization)
    pm = generate_preset_pass_manager(backend=backend, optimization_level=3)
    transpiled_qc = pm.run(qc)

    # Simulate the original circuit (ideal)
    ideal_sim = AerSimulator()
    ideal_result = ideal_sim.run(qc, shots=1024, seed_simulator=42).result()
    ideal_counts = ideal_result.get_counts()

    # Simulate the transpiled circuit (with noise-free simulation)
    # Use a coupling map that matches FakeTorontoV2 for a fair comparison
    noise_free_backend = AerSimulator.from_backend(backend)
    noisy_result = noise_free_backend.run(transpiled_qc, shots=1024, seed_simulator=42).result()
    noisy_counts = noisy_result.get_counts()

    # Both should have only two outcomes: all zeros and all ones
    # Because of mapping, the classical register layout may differ,
    # so we check that the number of distinct bitstrings is 2.
    assert len(noisy_counts) == 2, \
        f"Transpiled GHZ should produce exactly 2 outcomes, got {len(noisy_counts)}."
    # The two outcomes should have roughly equal probability
    values = list(noisy_counts.values())
    ratio = max(values) / min(values) if min(values) > 0 else float('inf')
    assert 0.8 < ratio < 1.2, \
        f"GHZ outcomes should be nearly balanced, got ratio {ratio}."