# SYNTACTIC tests — Qiskit HumanEval task task_0020
# Generated: 2026-04-28T12:35:30.590079
# Model: openai/gpt-5.4 (gpt54)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    result.remove_final_measurements()\n    backend = FakePerth()\n    assert result.num_qubits == backend.num_qubits\n    assert result.layout.initial_index_layout()[:3] == [2, 4, 6]\n'
ENTRY_POINT_NAME = 'transpile_ghz_customlayout'
# --- Official check block end ---
def test_module_loads_and_entry_exists_1():
    import ast
    import builtins as _b

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    try:
        tree = ast.parse(sol)
    except Exception as exc:
        raise AssertionError(f"Solution source must be valid Python and parse with ast.parse, got error: {exc}")

    assert tree is not None, "ast.parse should return an AST tree for valid solution source."
    assert isinstance(entry, str) and entry, "Injected entry point must be a non-empty string."

    g = {"__builtins__": __builtins__}
    try:
        exec(sol, g)
    except Exception as exc:
        raise AssertionError(f"Executing the solution source should succeed without import-time errors, got: {exc}")

    assert entry in g, f"Executed module must define the entry point '{entry}'."
    assert callable(g[entry]), f"Entry point '{entry}' must be callable."


def test_entry_signature_and_name_2():
    import builtins as _b
    import inspect

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    g = {"__builtins__": __builtins__}
    try:
        exec(sol, g)
    except Exception as exc:
        raise AssertionError(f"Solution source must execute successfully before inspecting signature, got: {exc}")

    assert entry == "transpile_ghz_customlayout", "Injected entry point should match the task-specified function name."
    assert entry in g, f"Function '{entry}' must be present after exec."
    candidate = g[entry]
    assert callable(candidate), f"Object bound to '{entry}' must be callable."

    try:
        sig = inspect.signature(candidate)
    except Exception as exc:
        raise AssertionError(f"inspect.signature should succeed on the candidate function, got: {exc}")

    params = list(sig.parameters.values())
    assert len(params) == 0, f"Function '{entry}' should take no parameters, found signature {sig}."
    assert candidate.__name__ == entry, f"Function __name__ should be '{entry}', got '{candidate.__name__}'."

    doc = inspect.getdoc(candidate)
    assert doc is None or isinstance(doc, str), "Function docstring, if present, should be a string."


def test_import_structure_and_qiskit_symbols_3():
    import ast
    import builtins as _b

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    try:
        tree = ast.parse(sol)
    except Exception as exc:
        raise AssertionError(f"Solution source must parse successfully for structural inspection, got: {exc}")

    func_defs = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
    target_defs = [node for node in func_defs if node.name == entry]
    assert target_defs, f"Source should define a function named '{entry}'."
    assert len(target_defs) == 1, f"Source should define '{entry}' exactly once at module level."

    imported_names = set()
    imported_modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_modules.add(alias.name)
                imported_names.add(alias.asname or alias.name.split(".")[-1])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imported_modules.add(node.module)
            for alias in node.names:
                imported_names.add(alias.asname or alias.name)

    expected_any = {
        "QuantumCircuit",
        "FakePerth",
        "generate_preset_pass_manager",
    }
    assert expected_any.intersection(imported_names), (
        "Solution should plausibly import at least one task-relevant Qiskit symbol "
        "(e.g., QuantumCircuit, FakePerth, or generate_preset_pass_manager)."
    )

    g = {"__builtins__": __builtins__}
    try:
        exec(sol, g)
    except Exception as exc:
        raise AssertionError(f"Solution source should execute successfully for module-level validation, got: {exc}")

    candidate = g.get(entry)
    assert candidate is not None, f"Executed module must expose '{entry}'."
    assert callable(candidate), f"Exposed entry '{entry}' must be callable."