# SEMANTIC tests — Qiskit HumanEval task task_0063
# Generated: 2026-04-28T11:34:38.763097
# Model: deepseek/deepseek-v3.2 (deepseekv32)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from numpy.random import seed\n    seed(12345)\n    basis = [1, 0, 0, 1, 1]\n    circuit = QuantumCircuit(5)\n    circuit.x([3, 4])\n    circuit.h([0, 3, 4])\n    result = candidate(basis, circuit)\n    assert result == "1"\n'
ENTRY_POINT_NAME = 'bb84_circuit_generate_key'
# --- Official check block end ---
import builtins as _b
import numpy as np
import pytest

sol = _b.INJECTED_SOLUTION_CODE
entry = _b.INJECTED_ENTRY_POINT
_g = {"__builtins__": __builtins__}
exec(sol, _g)
candidate = _g[entry]

def test_bb84_key_length_1():
    """Test that the generated key length equals the number of qubits where sender's basis is 0 (Z-basis) and measurement is deterministic."""
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector
    import numpy as np

    # Create a 5-qubit circuit where sender prepares |0> or |+> depending on basis
    n = 5
    senders_basis = [0, 1, 0, 1, 0]  # 0 -> Z, 1 -> X
    qc = QuantumCircuit(n, n)
    for i in range(n):
        if senders_basis[i] == 1:
            qc.h(i)
        # No errors, no eavesdropper, receiver measures in same basis (simulated by standard measurement)
        qc.measure(i, i)

    key = candidate(senders_basis, qc)

    # Expected: when basis is Z (0), prepared state is |0> -> measurement yields 0 deterministically.
    # When basis is X (1), prepared state is |+> -> measurement yields 0 or 1 randomly.
    # The BB84 protocol discards bits where bases differ (but here we simulate identical bases).
    # The function should return a binary string of length n (or possibly filtered_).
    # According to problem statement, generate key from circuit and sender's basis.
    # We'll check it's a string of length n (since no basis mismatch simulation).
    assert isinstance(key, str), f"Key must be a string, got {type(key)}"
    assert len(key) == n, f"Key length must match number of qubits ({n}), got {len(key)}"
    # All characters must be '0' or '1'
    assert all(c in '01' for c in key), f"Key contains non-binary characters: {key}"
    # For Z-basis qubits (indices 0,2,4), measurement must be 0 because we prepared |0> and measured Z.
    for i, b in enumerate(senders_basis):
        if b == 0:
            assert key[i] == '0', f"Qubit {i} prepared in Z-basis |0> must yield key bit '0', got {key[i]}"

def test_bb84_key_with_random_measurements_2():
    """Test that key bits for X-basis qubits are random (50/50) over many trials with a fixed circuit."""
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator
    import numpy as np

    # Simple circuit: one qubit, X-basis (|+>), measure
    senders_basis = [1]
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)

    # Run candidate multiple times (since measurement is probabilistic)
    # But note: candidate is deterministic given the circuit_ Actually the circuit includes measurement,
    # and the candidate likely extracts counts from the circuit's measurement results.
    # However, the circuit is fixed; to get randomness we need to simulate execution.
    # The problem expects candidate to generate key from the circuit and sender's basis.
    # We'll interpret that as: candidate should run the circuit on a simulator and extract the key.
    # So we'll test that the candidate's output varies appropriately.
    # We'll use a mock approach: replace the backend with a deterministic one for testing.
    # Instead, we directly test that the candidate returns a single-bit string.
    # We'll run the candidate 100 times with a fresh circuit each time (same structure).
    keys = []
    for _ in range(100):
        qc2 = QuantumCircuit(1, 1)
        qc2.h(0)
        qc2.measure(0, 0)
        key = candidate(senders_basis, qc2)
        keys.append(key)
    # All keys should be '0' or '1'
    assert all(k in ('0', '1') for k in keys), f"Keys must be single-bit strings, got {set(keys)}"
    # Roughly 50/50 distribution (allow large tolerance due to low sample size)
    zeros = sum(1 for k in keys if k == '0')
    ones = len(keys) - zeros
    assert 30 <= zeros <= 70, f"Expected roughly 50 zeros out of 100, got {zeros}"
    assert 30 <= ones <= 70, f"Expected roughly 50 ones out of 100, got {ones}"

def test_bb84_key_with_mismatched_basis_simulation_3():
    """Test that the key generation works when circuit includes measurements in different bases (simulating receiver's basis)."""
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector
    import numpy as np

    # Sender prepares in Z or X basis.
    # Receiver measures in Z or X basis (simulated by adding Hadamard before measurement if receiver's basis is X).
    # We'll create a circuit where receiver's basis matches sender's basis for some qubits, mismatches for others.
    # The BB84 protocol discards mismatched bits. The candidate function should still return a string,
    # but we can check that for matched bases the result is deterministic.
    n = 4
    senders_basis = [0, 1, 0, 1]  # Z, X, Z, X
    receiver_basis = [0, 1, 1, 0]  # match, match, mismatch, mismatch
    qc = QuantumCircuit(n, n)
    for i in range(n):
        if senders_basis[i] == 1:
            qc.h(i)
        if receiver_basis[i] == 1:
            qc.h(i)  # change to X-basis measurement
        qc.measure(i, i)
        if receiver_basis[i] == 1:
            qc.h(i)  # undo for clarity (not needed)

    key = candidate(senders_basis, qc)
    assert isinstance(key, str), f"Key must be a string, got {type(key)}"
    assert len(key) == n, f"Key length must match number of qubits ({n}), got {len(key)}"
    assert all(c in '01' for c in key), f"Key contains non-binary characters: {key}"

    # For matched bases (indices 0 and 1), the result should be deterministic:
    # index 0: Z-basis |0> -> measure Z -> 0
    # index 1: X-basis |+> -> measure X -> 0 (because |+> is +1 eigenstate of X)
    # Actually, |+> measured in X-basis yields 0 deterministically (if we define X measurement outcome 0 for +1 eigenstate).
    # In Qiskit, measuring a qubit in X-basis (by adding H before Z-measurement) on |+> yields 0 or 1 with 50/50_ Wait:
    # State |+> = H|0>. If we apply H again then measure Z: H|+> = |0>, so outcome 0 deterministic.
    # So for matched X-basis, measurement outcome should be 0.
    # Let's verify:
    # For index 0: sender Z, receiver Z -> deterministic 0.
    # For index 1: sender X, receiver X -> deterministic 0.
    # Thus key[0] and key[1] should be '0'.
    assert key[0] == '0', f"Matched Z-basis qubit 0 must yield '0', got {key[0]}"
    assert key[1] == '0', f"Matched X-basis qubit 1 must yield '0', got {key[1]}"
    # For mismatched bases, outcomes are random, but we only check they are binary.