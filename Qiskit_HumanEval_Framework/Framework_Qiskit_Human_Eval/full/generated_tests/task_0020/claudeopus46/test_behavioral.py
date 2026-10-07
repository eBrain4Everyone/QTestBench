# BEHAVIORAL tests — Qiskit HumanEval task task_0020
# Generated: 2026-04-28T11:12:52.465590
# Model: anthropic/claude-opus-4-6 (claudeopus46)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    result.remove_final_measurements()\n    backend = FakePerth()\n    assert result.num_qubits == backend.num_qubits\n    assert result.layout.initial_index_layout()[:3] == [2, 4, 6]\n'
ENTRY_POINT_NAME = 'transpile_ghz_customlayout'
# --- Official check block end ---
def test_transpile_ghz_customlayout_1():
    """Test that the returned circuit is a valid QuantumCircuit transpiled for FakePerth."""
    import builtins as _b
    import numpy as np
    from qiskit import QuantumCircuit
    from qiskit_ibm_runtime.fake_provider import FakePerth

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    result = candidate()

    assert isinstance(result, QuantumCircuit), "Result must be a QuantumCircuit instance"

    backend = FakePerth()
    num_backend_qubits = backend.num_qubits
    assert result.num_qubits == num_backend_qubits, (
        f"Transpiled circuit should have {num_backend_qubits} qubits (full backend width), "
        f"got {result.num_qubits}"
    )


def test_transpile_ghz_customlayout_2():
    """Test that the transpiled circuit uses the custom initial layout [2, 4, 6] and preserves GHZ unitary on those qubits."""
    import builtins as _b
    import numpy as np
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    result = candidate()

    # Check layout info exists and maps to physical qubits [2, 4, 6]
    layout = result.layout
    assert layout is not None, "Transpiled circuit must have layout information"

    initial_layout = layout.initial_layout
    # The initial layout should map virtual qubits 0,1,2 of the original circuit to physical qubits 2,4,6
    physical_bits = []
    for virt_idx in range(3):
        # Find which physical qubit virtual qubit virt_idx is mapped to
        for phys_qubit, virt_qubit in initial_layout.get_physical_bits().items():
            if hasattr(virt_qubit, '_index'):
                idx = virt_qubit._index
            else:
                idx = virt_qubit
            if idx == virt_idx:
                physical_bits.append(phys_qubit)
                break

    physical_bits_sorted = sorted(physical_bits)
    assert physical_bits_sorted == [2, 4, 6], (
        f"Initial layout should map to physical qubits [2, 4, 6], got {physical_bits_sorted}"
    )


def test_transpile_ghz_customlayout_3():
    """Test that the transpiled circuit produces GHZ-like behavior: only |000> and |111> outcomes."""
    import builtins as _b
    import numpy as np
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    result = candidate()

    # Simulate the transpiled circuit to verify it produces a GHZ state
    sv = Statevector.from_label('0' * result.num_qubits)
    sv = sv.evolve(result)

    # The GHZ state on qubits 2, 4, 6 means those qubits should be entangled
    # Get probabilities dictionary
    probs = sv.probabilities_dict()

    # Filter to only look at qubits 2, 4, 6 (physical qubits used)
    # Use reduced density matrix / marginal probabilities
    target_qubits = [2, 4, 6]
    marginal_probs = sv.probabilities(target_qubits)

    # For a 3-qubit GHZ state, only |000> and |111> should have non-zero probability
    # marginal_probs is indexed by computational basis of the 3 target qubits
    # Index 0 = |000>, Index 7 = |111>
    ghz_prob = marginal_probs[0] + marginal_probs[7]
    assert np.isclose(ghz_prob, 1.0, atol=1e-6), (
        f"GHZ state should have all probability in |000> and |111> states, "
        f"but total GHZ probability is {ghz_prob}"
    )
    assert np.isclose(marginal_probs[0], 0.5, atol=1e-6), (
        f"|000> probability should be ~0.5, got {marginal_probs[0]}"
    )
    assert np.isclose(marginal_probs[7], 0.5, atol=1e-6), (
        f"|111> probability should be ~0.5, got {marginal_probs[7]}"
    )