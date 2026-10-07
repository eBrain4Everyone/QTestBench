# SEMANTIC tests — Qiskit HumanEval task task_0019
# Generated: 2026-04-28T11:11:31.968058
# Model: anthropic/claude-opus-4-6 (claudeopus46)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    result.remove_final_measurements()\n    backend = FakeTorontoV2()\n    # Check initial layout is not the trivial layout (this is very unlikely\n    # if transpiled with optimization level 3)\n    assert result.layout.initial_index_layout() != list(range(backend.num_qubits))\n    # Optimization level 3 should easily find circuits with depth < 200\n    assert result.depth() < 150\n'
ENTRY_POINT_NAME = 'transpile_circuit_maxopt'
# --- Official check block end ---
import pytest

def test_transpile_circuit_maxopt_1():
    """Test that the returned circuit is a QuantumCircuit transpiled for FakeTorontoV2 (27 qubits)."""
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    from qiskit import QuantumCircuit
    from qiskit_ibm_runtime.fake_provider import FakeTorontoV2

    result = candidate()

    assert isinstance(result, QuantumCircuit), \
        f"Expected a QuantumCircuit, got {type(result)}"

    backend = FakeTorontoV2()
    num_backend_qubits = backend.num_qubits  # 27 for FakeToronto

    assert result.num_qubits == num_backend_qubits, \
        f"Transpiled circuit should have {num_backend_qubits} qubits (mapped to backend), got {result.num_qubits}"


def test_transpile_circuit_maxopt_2():
    """Test that the transpiled circuit only uses basis gates of FakeTorontoV2."""
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    from qiskit_ibm_runtime.fake_provider import FakeTorontoV2

    result = candidate()
    backend = FakeTorontoV2()

    # Get basis gates from the backend target
    target = backend.target
    basis_gate_names = set(target.operation_names)
    # Also allow barrier, measure, delay, reset as they are standard directives
    allowed = basis_gate_names | {'barrier', 'measure', 'delay', 'reset', 'snapshot'}

    circuit_ops = set(result.count_ops().keys())
    unexpected = circuit_ops - allowed
    assert len(unexpected) == 0, \
        f"Circuit contains gates not in backend basis gates: {unexpected}. Allowed: {allowed}"


def test_transpile_circuit_maxopt_3():
    """Test that the transpiled circuit is functionally equivalent to an 11-qubit GHZ state
    on the qubits it uses (unitary equivalence up to ancilla/idle qubits)."""
    import builtins as _b
    import numpy as np
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector

    result = candidate()

    # The original circuit is an 11-qubit GHZ circuit.
    # After transpilation to 27 qubits, the GHZ state should be present
    # on some subset of 11 qubits.
    # We verify by simulating and checking that the statevector has
    # GHZ-like structure: only |00...0> and |11...1> have nonzero amplitude
    # on the active qubits.

    sv = Statevector.from_instruction(result)
    probs = sv.probabilities()

    # Find which qubits are active (not idle)
    # For a GHZ state on 11 qubits mapped to 27, we expect exactly 2 nonzero
    # probabilities in the full 27-qubit space (corresponding to all-0 and all-1
    # on the 11 active qubits, with idle qubits in |0>).
    nonzero_indices = np.where(probs > 1e-6)[0]

    assert len(nonzero_indices) == 2, \
        f"GHZ state should have exactly 2 computational basis states with nonzero probability, got {len(nonzero_indices)}"

    # One of them must be 0 (all zeros)
    assert 0 in nonzero_indices, \
        "One of the nonzero basis states should be |00...0>"

    # The other state should have exactly 11 bits set (the 11 active qubits)
    other_index = [idx for idx in nonzero_indices if idx != 0][0]
    num_bits_set = bin(other_index).count('1')
    assert num_bits_set == 11, \
        f"The other basis state should have exactly 11 qubits in |1> state (GHZ on 11 qubits), got {num_bits_set} bits set"

    # Check that probabilities are approximately 0.5 each
    assert np.allclose(probs[0], 0.5, atol=1e-4, rtol=1e-5), \
        f"Probability of |00...0> should be ~0.5, got {probs[0]}"
    assert np.allclose(probs[other_index], 0.5, atol=1e-4, rtol=1e-5), \
        f"Probability of the other GHZ basis state should be ~0.5, got {probs[other_index]}"