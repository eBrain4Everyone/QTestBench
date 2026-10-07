# SEMANTIC tests — Qiskit HumanEval task task_0063
# Generated: 2026-04-28T11:15:33.853545
# Model: anthropic/claude-opus-4-6 (claudeopus46)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from numpy.random import seed\n    seed(12345)\n    basis = [1, 0, 0, 1, 1]\n    circuit = QuantumCircuit(5)\n    circuit.x([3, 4])\n    circuit.h([0, 3, 4])\n    result = candidate(basis, circuit)\n    assert result == "1"\n'
ENTRY_POINT_NAME = 'bb84_circuit_generate_key'
# --- Official check block end ---
import pytest

def test_bb84_circuit_generate_key_1():
    """Test that the function returns a string of '0's and '1's with correct length."""
    import builtins as _b
    import numpy as np
    from qiskit import QuantumCircuit

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    # Create a simple 4-qubit circuit where sender uses basis [0, 0, 0, 0] (all Z-basis)
    # and encodes bits 0, 1, 0, 1
    n = 4
    senders_basis = [0, 0, 0, 0]
    bits = [0, 1, 0, 1]

    qc = QuantumCircuit(n, n)
    for i in range(n):
        if bits[i] == 1:
            qc.x(i)
        # Z-basis: no Hadamard applied by sender

    result = candidate(senders_basis, qc)

    assert isinstance(result, str), f"Expected return type str, got {type(result)}"
    assert len(result) == n, f"Expected key length {n}, got {len(result)}"
    assert all(c in '01' for c in result), f"Key should only contain '0' and '1', got {result}"


def test_bb84_circuit_generate_key_2():
    """Test that measuring in the same basis as the sender recovers the encoded bits."""
    import builtins as _b
    import numpy as np
    from qiskit import QuantumCircuit

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    # Sender uses Z-basis (0) for all qubits and encodes known bits
    # When receiver also measures in Z-basis (sender's basis = 0), the key should match the encoded bits
    n = 4
    senders_basis = [0, 0, 0, 0]
    encoded_bits = [1, 0, 1, 1]

    qc = QuantumCircuit(n, n)
    for i in range(n):
        if encoded_bits[i] == 1:
            qc.x(i)

    # Run multiple times to check consistency (deterministic case)
    results = set()
    for _ in range(5):
        key = candidate(senders_basis, qc.copy())
        results.add(key)

    # Since all bases match and no Hadamard is applied, measurement in Z-basis should be deterministic
    # The key should be the same every time
    assert len(results) == 1, f"Expected deterministic result for Z-basis encoding/measurement, got {results}"

    key = results.pop()
    # The key should match the encoded bits (order may depend on bit ordering convention)
    expected_key = ''.join(str(b) for b in encoded_bits)
    expected_key_reversed = expected_key[::-1]
    assert key == expected_key or key == expected_key_reversed, \
        f"Expected key '{expected_key}' or '{expected_key_reversed}', got '{key}'"


def test_bb84_circuit_generate_key_3():
    """Test with X-basis (Hadamard) encoding - sender's basis all 1."""
    import builtins as _b
    import numpy as np
    from qiskit import QuantumCircuit

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    # Sender uses X-basis (1) for all qubits
    # Encode |+> (bit=0 in X-basis) and |-> (bit=1 in X-basis)
    n = 3
    senders_basis = [1, 1, 1]
    encoded_bits = [0, 1, 0]

    qc = QuantumCircuit(n, n)
    for i in range(n):
        if encoded_bits[i] == 1:
            qc.x(i)
        qc.h(i)  # Apply Hadamard for X-basis encoding

    # When the function measures in the sender's basis (X-basis), it should recover the bits
    results = set()
    for _ in range(5):
        key = candidate(senders_basis, qc.copy())
        results.add(key)

    assert len(results) == 1, f"Expected deterministic result when measuring in matching X-basis, got {results}"

    key = results.pop()
    expected_key = ''.join(str(b) for b in encoded_bits)
    expected_key_reversed = expected_key[::-1]
    assert key == expected_key or key == expected_key_reversed, \
        f"Expected key '{expected_key}' or '{expected_key_reversed}', got '{key}'"