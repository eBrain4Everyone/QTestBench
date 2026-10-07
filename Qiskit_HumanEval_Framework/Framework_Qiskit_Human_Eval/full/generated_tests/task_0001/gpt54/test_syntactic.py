# SYNTACTIC tests — Qiskit HumanEval task task_0001
# Generated: 2026-04-28T12:26:56.986607
# Model: openai/gpt-5.4 (gpt54)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    assert isinstance(result, dict)\n    assert result.keys() == {"00", "11"}\n    assert 0.4 < (result["00"] / sum(result.values())) < 0.6\n'
ENTRY_POINT_NAME = 'run_bell_state_simulator'
# --- Official check block end ---
def test_module_loads_and_parses_1():
    import ast
    import builtins as _b

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    try:
        tree = ast.parse(sol)
    except SyntaxError as e:
        raise AssertionError(f"Injected solution code must parse successfully, but got SyntaxError: {e}") from e

    assert tree is not None, "AST parsing should produce a syntax tree object."
    assert isinstance(entry, str) and entry, "Injected entry point must be a non-empty string."


def test_exec_and_entry_callable_2():
    import builtins as _b

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}

    try:
        exec(sol, g)
    except Exception as e:
        raise AssertionError(f"Executing injected solution code should succeed without import or runtime errors, but got: {type(e).__name__}: {e}") from e

    assert entry in g, f"Executed module must define the entry point '{entry}'."
    candidate = g[entry]
    assert callable(candidate), f"Entry point '{entry}' must be callable."


def test_signature_and_name_plausibility_3():
    import builtins as _b
    import inspect

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)

    assert entry == "run_bell_state_simulator", "Injected entry point should match the task's specified function name."
    assert entry in g, "Expected function name must exist in executed globals."

    candidate = g[entry]
    sig = inspect.signature(candidate)
    params = list(sig.parameters.values())

    assert callable(candidate), "Resolved entry object must be callable."
    assert len(params) == 0, f"Function '{entry}' should take no arguments, but found {len(params)} parameter(s)."
    assert candidate.__name__ == entry, f"Function __name__ should be '{entry}', got '{candidate.__name__}' instead."