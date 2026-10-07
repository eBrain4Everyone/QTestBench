# SYNTACTIC tests — Qiskit HumanEval task task_0063
# Generated: 2026-04-28T11:15:13.355010
# Model: anthropic/claude-opus-4-6 (claudeopus46)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from numpy.random import seed\n    seed(12345)\n    basis = [1, 0, 0, 1, 1]\n    circuit = QuantumCircuit(5)\n    circuit.x([3, 4])\n    circuit.h([0, 3, 4])\n    result = candidate(basis, circuit)\n    assert result == "1"\n'
ENTRY_POINT_NAME = 'bb84_circuit_generate_key'
# --- Official check block end ---
import pytest

def test_module_parses_and_loads_1():
    """Test that the solution source code parses as valid Python AST."""
    import ast
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    # Should parse without SyntaxError
    tree = ast.parse(sol)
    assert tree is not None, "AST parsing returned None"
    assert isinstance(tree, ast.Module), "Parsed AST is not a Module node"


def test_entry_point_exists_and_callable_2():
    """Test that exec'ing the solution exposes the entry point as a callable."""
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    assert entry in g, f"Entry point '{entry}' not found in executed module namespace"
    candidate = g[entry]
    assert callable(candidate), f"Entry point '{entry}' is not callable"


def test_signature_accepts_expected_args_3():
    """Test that the function signature accepts senders_basis and circuit parameters."""
    import inspect
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    sig = inspect.signature(candidate)
    params = list(sig.parameters.keys())
    assert len(params) >= 2, (
        f"Expected at least 2 parameters (senders_basis, circuit), got {len(params)}: {params}"
    )
    # Check parameter names match expected interface
    assert params[0] == "senders_basis", (
        f"First parameter should be 'senders_basis', got '{params[0]}'"
    )
    assert params[1] == "circuit", (
        f"Second parameter should be 'circuit', got '{params[1]}'"
    )