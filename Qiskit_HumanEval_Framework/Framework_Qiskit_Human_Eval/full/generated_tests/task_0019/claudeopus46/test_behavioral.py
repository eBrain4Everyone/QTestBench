# BEHAVIORAL tests — Qiskit HumanEval task task_0019
# Generated: 2026-04-28T11:11:55.200804
# Model: anthropic/claude-opus-4-6 (claudeopus46)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    result.remove_final_measurements()\n    backend = FakeTorontoV2()\n    # Check initial layout is not the trivial layout (this is very unlikely\n    # if transpiled with optimization level 3)\n    assert result.layout.initial_index_layout() != list(range(backend.num_qubits))\n    # Optimization level 3 should easily find circuits with depth < 200\n    assert result.depth() < 150\n'
ENTRY_POINT_NAME = 'transpile_circuit_maxopt'
# --- Official check block end ---
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
        f"Expected QuantumCircuit, got {type(result)}"

    backend = FakeTorontoV2()
    num_backend_qubits = backend.num_qubits

    # The transpiled circuit should have the same number of qubits as the backend (27 for Toronto)
    assert result.num_qubits == num_backend_qubits, \
        f"Expected {num_backend_qubits} qubits (FakeTorontoV2), got {result.num_qubits}"


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

    # Also allow barrier, measure, delay, reset as they are standard non-basis instructions
    allowed_extras = {'barrier', 'measure', 'delay', 'reset', 'snapshot', 'if_else', 'switch_case', 'for_loop', 'while_loop'}
    allowed_gates = basis_gate_names | allowed_extras

    circuit_gate_names = set(result.count_ops().keys())
    disallowed = circuit_gate_names - allowed_gates

    assert len(disallowed) == 0, \
        f"Circuit contains gates not in backend basis gates: {disallowed}. Allowed: {allowed_gates}"


def test_transpile_circuit_maxopt_3():
    """Test that the transpiled circuit preserves the GHZ state functionality (unitary equivalence on active qubits)."""
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

    # The transpiled circuit should have been generated from an 11-qubit GHZ circuit
    # We verify by simulating the statevector and checking the GHZ property:
    # The state should have non-zero amplitudes only for |00...0> and |11...1> on the active qubits.

    # Remove any measurements if present for statevector simulation
    circuit_no_meas = result.remove_final_measurements(inplace=False)

    sv = Statevector.from_instruction(circuit_no_meas)
    probs = sv.probabilities()

    # Find which qubits are actually used (non-idle)
    # For GHZ on 11 qubits mapped to 27 qubit backend, there should be 11 active qubits
    # The GHZ state should have only 2 non-zero probability entries
    nonzero_probs = probs[probs > 1e-8]

    # A GHZ state on 11 qubits should have exactly 2 non-zero probability entries
    # each approximately 0.5
    assert len(nonzero_probs) == 2, \
        f"Expected exactly 2 non-zero probability entries for GHZ state, got {len(nonzero_probs)}"

    assert np.allclose(nonzero_probs, [0.5, 0.5], atol=1e-6), \
        f"Expected probabilities [0.5, 0.5] for GHZ state, got {nonzero_probs}"

    # Verify that the non-zero entries correspond to all-0 and all-1 on 11 qubits
    nonzero_indices = np.where(probs > 1e-8)[0]
    # One should be 0 (all zeros state)
    assert 0 in nonzero_indices, \
        f"Expected |0...0> to have non-zero amplitude in GHZ state, nonzero indices: {nonzero_indices}"

    # The other should be all-1s on exactly 11 qubits (the active ones)
    other_idx = [idx for idx in nonzero_indices if idx != 0][0]
    binary_rep = bin(other_idx)[2:]
    num_ones = binary_rep.count('1')
    assert num_ones == 11, \
        f"Expected the other GHZ basis state to have 11 ones, got {num_ones} (index={other_idx}, binary={binary_rep})"