# BEHAVIORAL tests — Qiskit HumanEval task task_0063
# Generated: 2026-04-28T11:35:51.727777
# Model: deepseek/deepseek-v3.2 (deepseekv32)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from numpy.random import seed\n    seed(12345)\n    basis = [1, 0, 0, 1, 1]\n    circuit = QuantumCircuit(5)\n    circuit.x([3, 4])\n    circuit.h([0, 3, 4])\n    result = candidate(basis, circuit)\n    assert result == "1"\n'
ENTRY_POINT_NAME = 'bb84_circuit_generate_key'
# --- Official check block end ---
import builtins as _b
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

sol = _b.INJECTED_SOLUTION_CODE
entry = _b.INJECTED_ENTRY_POINT
_g = {"__builtins__": __builtins__}
exec(sol, _g)
candidate = _g[entry]


def test_bb84_deterministic_measurement_1():
    """Test that for matching bases the key bit is deterministic (0 or 1) according to initial state."""
    # Simulate a single qubit prepared in |0> (basis 0) or |1> (basis 0) or plus/minus states
    # We'll test four cases: (prep_basis, senders_basis, prep_state) -> expected deterministic outcome
    # prep_basis 0: computational, |0> -> 0, |1> -> 1
    # prep_basis 1: Hadamard, |+> -> 0 (if we measure in X basis and map + to 0), |-> -> 1
    # For matching bases, the measurement yields the prepared bit.
    from qiskit.quantum_info import Statevector

    test_cases = [
        # (prep_basis, prep_bit, senders_basis, expected_key_bit)
        (0, 0, [0], "0"),  # |0> measured in Z -> 0
        (0, 1, [0], "1"),  # |1> measured in Z -> 1
        (1, 0, [1], "0"),  # |+> measured in X -> 0 (conventional mapping)
        (1, 1, [1], "1"),  # |-> measured in X -> 1
    ]

    for prep_basis, prep_bit, senders_basis, expected in test_cases:
        qc = QuantumCircuit(1, 1)
        if prep_basis == 0:
            # computational basis encoding
            if prep_bit == 1:
                qc.x(0)
        else:
            # Hadamard basis encoding
            if prep_bit == 0:
                qc.h(0)  # |+>
            else:
                qc.x(0)
                qc.h(0)  # |->
        # Call the candidate to extract key
        key = candidate(senders_basis, qc)
        assert key == expected, f"Prep basis {prep_basis}, prep bit {prep_bit}, senders_basis {senders_basis} -> key '{key}' != expected '{expected}'"


def test_bb84_random_but_consistent_2():
    """Test that for mismatched bases the result is random but consistent across multiple runs of same circuit."""
    # When bases differ, measurement outcome is random 0/1.
    # Run the circuit multiple times with a fixed simulator seed and ensure the key bit is stable for that seed.
    # Create a circuit that prepares |0> in basis 0, but sender's basis is 1 (Hadamard).
    # The measurement in X basis yields random outcome.
    # We'll run the candidate twice with same circuit and same seed; they should give same key.
    qc = QuantumCircuit(1, 1)
    # Prepare |0> in computational basis
    # No gate needed
    senders_basis = [1]  # measure in X basis

    # First call
    key1 = candidate(senders_basis, qc)
    # Second call (candidate should not modify circuit in place, but if it does we need a fresh copy)
    qc2 = QuantumCircuit(1, 1)
    key2 = candidate(senders_basis, qc2)
    # Both should be either "0" or "1"
    assert key1 in ("0", "1"), f"Key '{key1}' not a valid bit string"
    assert key2 in ("0", "1"), f"Key '{key2}' not a valid bit string"
    # Since the circuit is identical and candidate uses a fixed measurement basis, outcome should be deterministic for that seed.
    # However, if candidate uses random sampling, the key might differ. We'll enforce that they are equal because we expect deterministic simulation.
    # We'll assume candidate uses a simulator with a fixed seed or deterministic outcome.
    assert key1 == key2, f"Two calls with identical deterministic circuit gave different keys: '{key1}' vs '{key2}'"


def test_bb84_multiple_qubits_3():
    """Test that the function works for multiple qubits, returning a string of length equal to number of qubits."""
    # Create a random circuit with 5 qubits, random preparation (some in Z, some in X),
    # and random sender's bases. Use a fixed seed for reproducibility.
    np.random.seed(42)
    n = 5
    prep_bases = np.random.randint(0, 2, n)
    prep_bits = np.random.randint(0, 2, n)
    senders_bases = np.random.randint(0, 2, n)

    qc = QuantumCircuit(n, n)
    for i in range(n):
        if prep_bases[i] == 0:
            if prep_bits[i] == 1:
                qc.x(i)
        else:
            if prep_bits[i] == 0:
                qc.h(i)
            else:
                qc.x(i)
                qc.h(i)

    key = candidate(list(senders_bases), qc)
    # Check that key is a string of length n
    assert isinstance(key, str), f"Key must be a string, got {type(key)}"
    assert len(key) == n, f"Key length {len(key)} != number of qubits {n}"
    # Each character must be '0' or '1'
    for ch in key:
        assert ch in ('0', '1'), f"Invalid character '{ch}' in key '{key}'"
    # Additionally, for qubits where prep_basis == senders_basis, the key bit should equal prep_bit.
    for i in range(n):
        if prep_bases[i] == senders_bases[i]:
            expected_bit = str(prep_bits[i])
            actual_bit = key[i]
            assert actual_bit == expected_bit, f"Qubit {i}: bases match, expected {expected_bit} but got {actual_bit}. Full key: {key}"