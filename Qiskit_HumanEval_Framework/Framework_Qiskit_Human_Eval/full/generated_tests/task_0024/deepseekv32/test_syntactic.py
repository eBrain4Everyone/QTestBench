# SYNTACTIC tests — Qiskit HumanEval task task_0024
# Generated: 2026-04-28T11:27:09.673426
# Model: deepseek/deepseek-v3.2 (deepseekv32)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    balanced = QuantumCircuit(5)\n    balanced.cx(3, 4)\n    assert candidate(balanced) == False\n    constant = QuantumCircuit(9)\n    constant.x(8)\n    assert candidate(constant) == True\n'
ENTRY_POINT_NAME = 'dj_algorithm'
# --- Official check block end ---
import builtins as _b
import sys
import inspect
import ast

def test_module_import_and_entry_point_exists():
    """Check that the solution code can be parsed and the entry point exists and is callable."""
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    # Parse should succeed
    ast.parse(sol)
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    # Entry point must exist in the namespace
    assert entry in g, f"Entry point '{entry}' not found in the solution module"
    candidate = g[entry]
    # Must be callable
    assert callable(candidate), f"'{entry}' is not callable"
    # Should have expected name (optional)
    assert candidate.__name__ == entry, f"Function name mismatch: expected '{entry}', got '{candidate.__name__}'"

def test_signature_matches_problem():
    """Verify the signature matches the problem statement: one QuantumCircuit argument, returns bool."""
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    sig = inspect.signature(candidate)
    params = list(sig.parameters.items())
    # Exactly one parameter
    assert len(params) == 1, f"Expected exactly one parameter, got {len(params)}"
    param_name, param = params[0]
    # Parameter should be named 'oracle' (or at least be a single parameter)
    # We'll just check type annotation if present, but not require it.
    # Return annotation should be bool (optional)
    if sig.return_annotation is not sig.empty:
        assert sig.return_annotation is bool, f"Return annotation must be bool, got {sig.return_annotation}"
    # Check that the function can be called with a QuantumCircuit (import here)
    from qiskit import QuantumCircuit
    dummy_qc = QuantumCircuit(3)
    # Should not raise TypeError on call with a QuantumCircuit
    try:
        candidate(dummy_qc)
    except TypeError as e:
        raise AssertionError(f"Call with QuantumCircuit raised TypeError: {e}") from e
    # Return type not enforced here because we didn't run the algorithm.

def test_solution_uses_required_imports():
    """Check that the solution uses necessary imports (qiskit)."""
    sol = _b.INJECTED_SOLUTION_CODE
    # Ensure that the code does not contain obvious syntax errors beyond parse.
    # We'll just check that the solution code is non_empty and contains 'QuantumCircuit' (optional, not required).
    # Minimal check: the solution is a string.
    assert isinstance(sol, str), "Solution code must be a string"
    assert len(sol.strip()) > 0, "Solution code is empty"
    # We can also verify that the solution does not crash on import of its own module.
    g = {"__builtins__": __builtins__}
    try:
        exec(sol, g)
    except Exception as e:
        raise AssertionError(f"Solution code raised an exception during exec: {e}") from e
    # Ensure the entry point is present after exec (redundant but safe)
    entry = _b.INJECTED_ENTRY_POINT
    assert entry in g, f"Entry point '{entry}' missing after exec"