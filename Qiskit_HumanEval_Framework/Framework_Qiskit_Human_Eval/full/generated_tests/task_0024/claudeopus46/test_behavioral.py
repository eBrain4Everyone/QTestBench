# BEHAVIORAL tests — Qiskit HumanEval task task_0024
# Generated: 2026-04-28T11:13:34.685636
# Model: anthropic/claude-opus-4-6 (claudeopus46)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    balanced = QuantumCircuit(5)\n    balanced.cx(3, 4)\n    assert candidate(balanced) == False\n    constant = QuantumCircuit(9)\n    constant.x(8)\n    assert candidate(constant) == True\n'
ENTRY_POINT_NAME = 'dj_algorithm'
# --- Official check block end ---
def test_constant_zero_oracle_1():
    """Test that a constant-0 oracle (identity on output qubit) is detected as constant."""
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    from qiskit import QuantumCircuit

    # Constant-0 oracle: does nothing (f(x) = 0 for all x)
    # 2 input qubits + 1 output qubit = 3 qubits total
    oracle = QuantumCircuit(3)
    # No gates _ output qubit is never flipped, so f(x) = 0 for all x (constant)

    result = candidate(oracle)
    assert result is True or result == True, (
        f"Expected True (constant) for constant-0 oracle, got {result}"
    )


def test_constant_one_oracle_2():
    """Test that a constant-1 oracle (always flips output qubit) is detected as constant."""
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    from qiskit import QuantumCircuit

    # Constant-1 oracle: f(x) = 1 for all x
    # 3 input qubits + 1 output qubit = 4 qubits total
    oracle = QuantumCircuit(4)
    # Just flip the output qubit (last qubit, index 3) unconditionally
    oracle.x(3)

    result = candidate(oracle)
    assert result is True or result == True, (
        f"Expected True (constant) for constant-1 oracle, got {result}"
    )


def test_balanced_oracle_3():
    """Test that balanced oracles are correctly detected as not constant."""
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    from qiskit import QuantumCircuit

    # Balanced oracle using CNOT: f(x) = x_0 (parity of first qubit)
    # 2 input qubits + 1 output qubit = 3 qubits
    oracle_balanced_1 = QuantumCircuit(3)
    oracle_balanced_1.cx(0, 2)  # output qubit (index 2) flipped when qubit 0 is |1>

    result1 = candidate(oracle_balanced_1)
    assert result1 is False or result1 == False, (
        f"Expected False (balanced) for CNOT-based balanced oracle on qubit 0, got {result1}"
    )

    # Another balanced oracle: f(x) = x_1
    oracle_balanced_2 = QuantumCircuit(3)
    oracle_balanced_2.cx(1, 2)  # output qubit flipped when qubit 1 is |1>

    result2 = candidate(oracle_balanced_2)
    assert result2 is False or result2 == False, (
        f"Expected False (balanced) for CNOT-based balanced oracle on qubit 1, got {result2}"
    )

    # Balanced oracle with XOR of all inputs: f(x) = x_0 XOR x_1
    # For 2 input qubits, this is balanced (half 0, half 1)
    oracle_balanced_3 = QuantumCircuit(3)
    oracle_balanced_3.cx(0, 2)
    oracle_balanced_3.cx(1, 2)

    result3 = candidate(oracle_balanced_3)
    assert result3 is False or result3 == False, (
        f"Expected False (balanced) for XOR balanced oracle, got {result3}"
    )

    # Test with single input qubit (1 input + 1 output = 2 qubits)
    # Balanced: f(x) = x
    oracle_1qubit = QuantumCircuit(2)
    oracle_1qubit.cx(0, 1)

    result4 = candidate(oracle_1qubit)
    assert result4 is False or result4 == False, (
        f"Expected False (balanced) for single-qubit balanced oracle, got {result4}"
    )