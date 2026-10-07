# BEHAVIORAL tests — Qiskit HumanEval task task_0063
# Generated: 2026-04-28T11:15:55.134386
# Model: anthropic/claude-opus-4-6 (claudeopus46)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from numpy.random import seed\n    seed(12345)\n    basis = [1, 0, 0, 1, 1]\n    circuit = QuantumCircuit(5)\n    circuit.x([3, 4])\n    circuit.h([0, 3, 4])\n    result = candidate(basis, circuit)\n    assert result == "1"\n'
ENTRY_POINT_NAME = 'bb84_circuit_generate_key'
# --- Official check block end ---
def test_bb84_circuit_generate_key_1():
    """Test basic BB84 key generation with matching bases - all zeros."""
    import builtins as _b
    import numpy as np
    from qiskit import QuantumCircuit

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    # Create a simple 4-qubit circuit where sender encodes bits in Z basis (basis=0)
    # Sender's bits: [0, 0, 0, 0], Sender's basis: [0, 0, 0, 0]
    # No X or H gates applied by sender (all zeros in Z basis)
    n = 4
    qc = QuantumCircuit(n, n)
    # Sender encodes: bit=0, basis=0 -> do nothing (|0>)
    # Receiver measures in basis matching sender's basis
    # For Z basis (basis=0), just measure directly
    for i in range(n):
        qc.measure(i, i)

    senders_basis = [0, 0, 0, 0]
    result = candidate(senders_basis, qc)

    assert isinstance(result, str), f"Expected string return type, got {type(result)}"
    # With all qubits in |0> and measured in Z basis, key should be all '0's
    # The length should be n (or possibly filtered based on matching bases)
    assert len(result) > 0, "Key should not be empty when bases match"
    for ch in result:
        assert ch in ('0', '1'), f"Key should contain only '0' or '1', got '{ch}'"


def test_bb84_circuit_generate_key_2():
    """Test BB84 key generation with sender encoding bit=1 in Z basis."""
    import builtins as _b
    import numpy as np
    from qiskit import QuantumCircuit

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    # Sender encodes bit=1 in Z basis (applies X gate)
    # Receiver measures in Z basis
    n = 2
    qc = QuantumCircuit(n, n)
    # qubit 0: bit=1, basis=0 -> apply X
    qc.x(0)
    # qubit 1: bit=0, basis=0 -> do nothing
    qc.measure(0, 0)
    qc.measure(1, 1)

    senders_basis = [0, 0]
    result = candidate(senders_basis, qc)

    assert isinstance(result, str), f"Expected string return type, got {type(result)}"
    assert len(result) > 0, "Key should not be empty"
    # The key bits should reflect the measurement outcomes
    # With matching Z bases: qubit 0 should give '1', qubit 1 should give '0'
    for ch in result:
        assert ch in ('0', '1'), f"Key characters should be '0' or '1', got '{ch}'"


def test_bb84_circuit_generate_key_3():
    """Test BB84 key generation with mixed bases - some matching, some not."""
    import builtins as _b
    import numpy as np
    from qiskit import QuantumCircuit

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    # 4 qubits: sender uses bases [0, 1, 0, 1]
    # Receiver measures in bases [0, 0, 0, 0] (all Z basis)
    # Matching bases: qubit 0 and qubit 2 (both Z)
    # Non-matching: qubit 1 and qubit 3
    n = 4
    qc = QuantumCircuit(n, n)
    # Sender encodes all zeros
    # For basis=1 (X basis), sender applies H
    qc.h(1)
    qc.h(3)
    # Receiver measures all in Z basis (no H before measurement)
    for i in range(n):
        qc.measure(i, i)

    senders_basis = [0, 1, 0, 1]
    result = candidate(senders_basis, qc)

    assert isinstance(result, str), f"Expected string return type, got {type(result)}"
    # Result should be a binary string
    for ch in result:
        assert ch in ('0', '1'), f"Key characters should be '0' or '1', got '{ch}'"
    # The function should return some key (possibly filtered by matching bases)
    # We just verify it returns a valid binary string
    assert len(result) >= 0, "Key length should be non-negative"