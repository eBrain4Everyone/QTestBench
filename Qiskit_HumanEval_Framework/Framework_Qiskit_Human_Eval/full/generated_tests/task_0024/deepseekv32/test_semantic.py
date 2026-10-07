# SEMANTIC tests — Qiskit HumanEval task task_0024
# Generated: 2026-04-28T11:27:23.904504
# Model: deepseek/deepseek-v3.2 (deepseekv32)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    balanced = QuantumCircuit(5)\n    balanced.cx(3, 4)\n    assert candidate(balanced) == False\n    constant = QuantumCircuit(9)\n    constant.x(8)\n    assert candidate(constant) == True\n'
ENTRY_POINT_NAME = 'dj_algorithm'
# --- Official check block end ---
import builtins as _b
import numpy as np
import pytest

sol = _b.INJECTED_SOLUTION_CODE
entry = _b.INJECTED_ENTRY_POINT
g = {"__builtins__": __builtins__}
exec(sol, g)
candidate = g[entry]


def test_dj_algorithm_constant_oracle_returns_true_1():
    """Test that a constant 0 oracle returns True."""
    import qiskit.circuit.library as qclib

    n = 3
    oracle = QuantumCircuit(n + 1)
    # constant 0 oracle: identity on all qubits, output qubit unchanged
    oracle.id(range(n + 1))
    result = candidate(oracle)
    assert result is True, f"Constant 0 oracle should return True, got {result}"


def test_dj_algorithm_constant_oracle_returns_true_2():
    """Test that a constant 1 oracle returns True."""
    import qiskit.circuit.library as qclib

    n = 4
    oracle = QuantumCircuit(n + 1)
    # constant 1 oracle: flip output qubit (last qubit) for all inputs
    oracle.x(n)
    result = candidate(oracle)
    assert result is True, f"Constant 1 oracle should return True, got {result}"


def test_dj_algorithm_balanced_oracle_returns_false_3():
    """Test that a balanced oracle returns False."""
    import qiskit.circuit.library as qclib

    n = 2
    oracle = QuantumCircuit(n + 1)
    # balanced oracle: XOR of first input qubit onto output qubit
    oracle.cx(0, n)
    result = candidate(oracle)
    assert result is False, f"Balanced oracle should return False, got {result}"