# SYNTACTIC tests — Qiskit HumanEval task task_0002
# Generated: 2026-04-28T12:28:30.028230
# Model: openai/gpt-5.4 (gpt54)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    solution = (Statevector.from_label("00") + Statevector.from_label("11")) / sqrt(2)\n    assert result.equiv(solution)\n'
ENTRY_POINT_NAME = 'create_bell_statevector'
# --- Official check block end ---
def test_module_parses_and_executes_1():
    import ast
    import builtins as _b

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    try:
        tree = ast.parse(sol)
    except SyntaxError as e:
        assert False, f"Injected solution code must parse without SyntaxError, got: {e}"

    assert tree is not None, "ast.parse should return an AST tree for valid solution code."
    assert isinstance(entry, str) and entry, "Injected entry point must be a non-empty string."

    g = {"__builtins__": __builtins__}
    try:
        exec(sol, g)
    except Exception as e:
        assert False, f"Executing injected solution code should not raise an exception, got: {e}"

    assert entry in g, f"Executed module must define the entry point name '{entry}'."
    assert callable(g[entry]), f"Object bound to entry point '{entry}' must be callable."


def test_entry_point_signature_and_name_2():
    import builtins as _b
    import inspect

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    g = {"__builtins__": __builtins__}
    try:
        exec(sol, g)
    except Exception as e:
        assert False, f"Solution code must execute successfully before signature inspection, got: {e}"

    assert entry == "create_bell_statevector", (
        f"Task entry point should be 'create_bell_statevector', got '{entry}'."
    )
    assert entry in g, f"Global namespace after exec must contain '{entry}'."

    candidate = g[entry]
    assert callable(candidate), f"Entry point '{entry}' must be callable."

    try:
        sig = inspect.signature(candidate)
    except Exception as e:
        assert False, f"inspect.signature should succeed on the candidate function, got: {e}"

    params = list(sig.parameters.values())
    assert len(params) == 0, (
        f"create_bell_statevector should take no parameters, found {len(params)} parameter(s)."
    )


def test_basic_plausibility_and_imports_3():
    import builtins as _b
    import inspect

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    assert "Statevector" in sol, (
        "Solution source should plausibly reference Statevector for this task."
    )

    g = {"__builtins__": __builtins__}
    try:
        exec(sol, g)
    except Exception as e:
        assert False, f"Solution code must exec successfully for plausibility checks, got: {e}"

    assert entry in g, f"Executed solution must expose '{entry}' in globals."
    candidate = g[entry]
    assert callable(candidate), f"'{entry}' must resolve to a callable."

    doc = inspect.getdoc(candidate)
    assert doc is None or isinstance(doc, str), (
        "Function docstring, if present, must be a string."
    )

    module_name = getattr(candidate, "__module__", None)
    assert module_name is not None, (
        "Candidate function should have a __module__ attribute after execution."
    )