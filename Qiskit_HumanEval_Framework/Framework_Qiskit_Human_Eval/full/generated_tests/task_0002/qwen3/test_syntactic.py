# SYNTACTIC tests — Qiskit HumanEval task task_0002
# Generated: 2026-04-28T12:39:19.280394
# Model: qwen/qwen3-coder-next (qwen3)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    solution = (Statevector.from_label("00") + Statevector.from_label("11")) / sqrt(2)\n    assert result.equiv(solution)\n'
ENTRY_POINT_NAME = 'create_bell_statevector'
# --- Official check block end ---
import pytest
import ast
import inspect
import builtins as _b

# Load solution and entry point
sol = _b.INJECTED_SOLUTION_CODE
entry = _b.INJECTED_ENTRY_POINT

def test_module_syntax_and_load():
    # Test that the solution parses correctly
    ast.parse(sol)
    
    # Test that execution succeeds
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    
    # Verify entry point exists and is callable
    assert entry in g
    assert callable(g[entry])

def test_entry_point_name_and_callable():
    # Re-execute to ensure fresh namespace
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    
    # Check the specific expected function name
    assert "create_bell_statevector" in g
    func = g["create_bell_statevector"]
    assert callable(func)

def test_function_signature_and_return_type():
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    
    func = g[entry]
    
    # Check signature accepts no arguments (as per example)
    sig = inspect.signature(func)
    assert len(sig.parameters) == 0, "Function should take no arguments"
    
    # Call and check return type
    from qiskit.quantum_info import Statevector
    result = func()
    assert isinstance(result, Statevector), "Return value must be a Statevector instance"