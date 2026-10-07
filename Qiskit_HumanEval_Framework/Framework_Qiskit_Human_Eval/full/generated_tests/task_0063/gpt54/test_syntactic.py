# SYNTACTIC tests — Qiskit HumanEval task task_0063
# Generated: 2026-04-28T12:38:14.076257
# Model: openai/gpt-5.4 (gpt54)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from numpy.random import seed\n    seed(12345)\n    basis = [1, 0, 0, 1, 1]\n    circuit = QuantumCircuit(5)\n    circuit.x([3, 4])\n    circuit.h([0, 3, 4])\n    result = candidate(basis, circuit)\n    assert result == "1"\n'
ENTRY_POINT_NAME = 'bb84_circuit_generate_key'
# --- Official check block end ---
def test_module_loads_and_entry_exists_1():
    import ast
    import builtins as _b

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    try:
        tree = ast.parse(sol)
    except SyntaxError as e:
        raise AssertionError(f"Solution source must parse without SyntaxError, got: {e}") from e

    assert tree is not None, "ast.parse should return an AST tree for valid solution source."

    g = {"__builtins__": __builtins__}
    try:
        exec(sol, g)
    except Exception as e:
        raise AssertionError(f"Executing solution source should not fail, got: {type(e).__name__}: {e}") from e

    assert entry in g, f"Entry point '{entry}' must be defined in the executed module namespace."
    assert callable(g[entry]), f"Entry point '{entry}' must be callable."


def test_signature_plausibility_2():
    import builtins as _b
    import inspect

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    assert callable(candidate), f"Resolved entry point '{entry}' must be callable before signature inspection."

    sig = inspect.signature(candidate)
    params = list(sig.parameters.values())

    assert len(params) == 2, (
        f"Function '{entry}' should accept exactly 2 parameters "
        f"(senders_basis, circuit); got {len(params)}."
    )
    assert params[0].kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD), (
        f"First parameter of '{entry}' should be positional-compatible; got kind {params[0].kind}."
    )
    assert params[1].kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD), (
        f"Second parameter of '{entry}' should be positional-compatible; got kind {params[1].kind}."
    )
    assert params[0].name == "senders_basis", (
        f"First parameter should be named 'senders_basis'; got '{params[0].name}'."
    )
    assert params[1].name == "circuit", (
        f"Second parameter should be named 'circuit'; got '{params[1].name}'."
    )


def test_imports_and_definition_structure_3():
    import ast
    import builtins as _b

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    tree = ast.parse(sol)

    func_defs = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
    names = [node.name for node in func_defs]

    assert entry in names, f"Module source should define a top-level function named '{entry}'."

    target_defs = [node for node in func_defs if node.name == entry]
    assert len(target_defs) >= 1, f"Expected to find function definition for '{entry}' in AST."

    target = target_defs[0]
    assert len(target.args.args) == 2, (
        f"AST for '{entry}' should show exactly 2 declared positional parameters; "
        f"got {len(target.args.args)}."
    )

    g = {"__builtins__": __builtins__}
    try:
        exec(sol, g)
    except Exception as e:
        raise AssertionError(f"Solution module should execute successfully for structural validation, got: {e}") from e

    candidate = g.get(entry, None)
    assert candidate is not None, f"After execution, namespace must contain '{entry}'."
    assert callable(candidate), f"After execution, '{entry}' must resolve to a callable object."