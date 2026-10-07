# SEMANTIC tests — Qiskit HumanEval task task_0024
# Generated: 2026-04-28T11:13:18.088609
# Model: anthropic/claude-opus-4-6 (claudeopus46)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    balanced = QuantumCircuit(5)\n    balanced.cx(3, 4)\n    assert candidate(balanced) == False\n    constant = QuantumCircuit(9)\n    constant.x(8)\n    assert candidate(constant) == True\n'
ENTRY_POINT_NAME = 'dj_algorithm'
# --- Official check block end ---
import pytest

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
    # 3 qubits: 2 input + 1 output
    oracle = QuantumCircuit(3)
    # No gates needed - output qubit unchanged means f(x)=0 for all x
    
    result = candidate(oracle)
    assert result is True or result == True, (
        f"Expected True (constant) for constant-0 oracle, got {result}"
    )


def test_constant_one_oracle_2():
    """Test that a constant-1 oracle (X on output qubit) is detected as constant."""
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    from qiskit import QuantumCircuit

    # Constant-1 oracle: flips output qubit regardless of input (f(x) = 1 for all x)
    # 4 qubits: 3 input + 1 output (last qubit is output)
    oracle = QuantumCircuit(4)
    oracle.x(3)  # Flip output qubit unconditionally
    
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

    # Balanced oracle using CNOT: f(x) = x_0
    # 2 qubits: 1 input + 1 output (qubit 1 is output)
    oracle_2q = QuantumCircuit(2)
    oracle_2q.cx(0, 1)  # output XORed with input qubit 0
    
    result_2q = candidate(oracle_2q)
    assert result_2q is False or result_2q == False, (
        f"Expected False (balanced) for CNOT balanced oracle (2 qubits), got {result_2q}"
    )

    # Balanced oracle with 3 qubits (2 input + 1 output): f(x) = x_0 XOR x_1
    oracle_3q = QuantumCircuit(3)
    oracle_3q.cx(0, 2)  # XOR with first input
    oracle_3q.cx(1, 2)  # XOR with second input
    
    result_3q = candidate(oracle_3q)
    assert result_3q is False or result_3q == False, (
        f"Expected False (balanced) for balanced oracle (3 qubits), got {result_3q}"
    )

    # Another balanced oracle: f(x) = x_0 (only depends on first qubit), 3 qubits
    oracle_3q_b = QuantumCircuit(3)
    oracle_3q_b.cx(0, 2)
    
    result_3q_b = candidate(oracle_3q_b)
    assert result_3q_b is False or result_3q_b == False, (
        f"Expected False (balanced) for single-CX balanced oracle (3 qubits), got {result_3q_b}"
    )