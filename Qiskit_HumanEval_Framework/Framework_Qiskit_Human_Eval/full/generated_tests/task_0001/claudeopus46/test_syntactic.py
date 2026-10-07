# SYNTACTIC tests — Qiskit HumanEval task task_0001
# Generated: 2026-04-28T11:08:52.227700
# Model: anthropic/claude-opus-4-6 (claudeopus46)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    assert isinstance(result, dict)\n    assert result.keys() == {"00", "11"}\n    assert 0.4 < (result["00"] / sum(result.values())) < 0.6\n'
ENTRY_POINT_NAME = 'run_bell_state_simulator'
# --- Official check block end ---
import ast
import inspect


def test_module_parses_and_loads_1():
    """Test that the solution source code is valid Python and can be parsed."""
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    # Check that the source parses as valid Python AST
    tree = ast.parse(sol)
    assert isinstance(tree, ast.Module), "Solution source should parse as an ast.Module"

    # Check that exec succeeds without errors
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    assert entry in g, f"Entry point '{entry}' should exist in the executed module namespace"


def test_entry_point_exists_and_callable_2():
    """Test that the entry point is callable and has the correct name."""
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    g = {"__builtins__": __builtins__}
    exec(sol, g)

    candidate = g[entry]
    assert callable(candidate), f"'{entry}' should be callable"
    assert entry == "run_bell_state_simulator", (
        f"Entry point should be 'run_bell_state_simulator', got '{entry}'"
    )


def test_signature_takes_no_arguments_3():
    """Test that run_bell_state_simulator takes no required arguments."""
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
        and p.kind not in (
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD,
        )
    ]
    assert len(required_params) == 0, (
        f"run_bell_state_simulator should take no required arguments, "
        f"but found required params: {[p.name for p in required_params]}"
    )