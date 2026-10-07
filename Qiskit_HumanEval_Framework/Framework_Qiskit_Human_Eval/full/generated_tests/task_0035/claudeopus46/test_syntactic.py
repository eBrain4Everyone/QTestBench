# SYNTACTIC tests — Qiskit HumanEval task task_0035
# Generated: 2026-04-28T11:14:39.224224
# Model: anthropic/claude-opus-4-6 (claudeopus46)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from numpy import isclose\n    job = candidate()\n    assert isinstance(job, PrimitiveJob)\n    assert job.job_id() is not None\n    result = job.result()\n    assert isclose(result[0].data.evs.item(), 0.33, atol=0.06)\n'
ENTRY_POINT_NAME = 'run_circuit_with_dd_trex'
# --- Official check block end ---
import pytest

def test_module_parses_1():
    """Test that the solution source code is valid Python (ast.parse succeeds)."""
    import ast
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    try:
        tree = ast.parse(sol)
    except SyntaxError as e:
        pytest.fail(f"Solution source code failed to parse: {e}")
    assert isinstance(tree, ast.Module), "ast.parse should return an ast.Module node"


def test_entry_point_exists_and_callable_2():
    """Test that exec(sol, g) succeeds and the entry point is present and callable."""
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    try:
        exec(sol, g)
    except Exception as e:
        pytest.fail(f"exec(sol, g) raised an exception: {e}")
    assert entry in g, f"Entry point '{entry}' not found in executed namespace"
    candidate = g[entry]
    assert callable(candidate), f"Entry point '{entry}' is not callable"


def test_signature_no_required_args_3():
    """Test that run_circuit_with_dd_trex takes no required arguments."""
    import inspect
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    sig = inspect.signature(candidate)
    required_params = [
        p for p in sig.parameters.values()
        if p.default is inspect.Parameter.empty
        and p.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
    ]
    assert len(required_params) == 0, (
        f"Expected run_circuit_with_dd_trex to have no required parameters, "
        f"but found {len(required_params)}: {[p.name for p in required_params]}"
    )