# SYNTACTIC tests — Qiskit HumanEval task task_0000
# Generated: 2026-04-28T11:16:25.109653
# Model: deepseek/deepseek-v3.2 (deepseekv32)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate(3)\n    assert isinstance(result, QuantumCircuit)\n    assert result.num_qubits == 3\n'
ENTRY_POINT_NAME = 'create_quantum_circuit'
# --- Official check block end ---
import builtins as _b
import ast
import inspect
import pytest
import sys

def test_valid_syntax_and_import_1():
    """Verify solution can be parsed and executed without syntax errors."""
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    # parse
    try:
        ast.parse(sol)
    except SyntaxError as e:
        pytest.fail(f"Solution has syntax error: {e}")
    # exec into clean namespace
    g = {"__builtins__": __builtins__}
    try:
        exec(sol, g)
    except Exception as e:
        pytest.fail(f"Executing solution raised: {e}")
    assert entry in g, f"Entry point '{entry}' not found after exec."
    assert callable(g[entry]), f"Entry point '{entry}' is not callable."

def test_signature_and_basic_call_2():
    """Check that the function accepts a single int argument and returns a QuantumCircuit."""
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    sig = inspect.signature(candidate)
    assert len(sig.parameters) == 1, f"Expected exactly one parameter, got {len(sig.parameters)}"
    param_name = list(sig.parameters.keys())[0]
    param = sig.parameters[param_name]
    # parameter may have no annotation; that's fine.
    # call it with a small integer
    try:
        result = candidate(3)
    except Exception as e:
        pytest.fail(f"Calling {entry}(3) raised: {e}")
    # The problem states return a QuantumCircuit, so verify type.
    from qiskit import QuantumCircuit
    assert isinstance(result, QuantumCircuit), f"Result is {type(result)} expected QuantumCircuit."

def test_circuit_properties_3():
    """Verify the returned circuit has the expected number of qubits."""
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    # test with two different sizes
    for n in [1, 5]:
        qc = candidate(n)
        from qiskit import QuantumCircuit
        assert isinstance(qc, QuantumCircuit), f"For n={n}, result is not a QuantumCircuit."
        assert qc.num_qubits == n, f"For n={n}, circuit has {qc.num_qubits} qubits."
        # also check that it has at least zero gates (no over_specification)
        # (any valid QuantumCircuit is acceptable)