# SYNTACTIC tests — Qiskit HumanEval task task_0019
# Generated: 2026-04-28T12:34:48.975861
# Model: openai/gpt-5.4 (gpt54)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    result.remove_final_measurements()\n    backend = FakeTorontoV2()\n    # Check initial layout is not the trivial layout (this is very unlikely\n    # if transpiled with optimization level 3)\n    assert result.layout.initial_index_layout() != list(range(backend.num_qubits))\n    # Optimization level 3 should easily find circuits with depth < 200\n    assert result.depth() < 150\n'
ENTRY_POINT_NAME = 'transpile_circuit_maxopt'
# --- Official check block end ---
def test_module_parses_and_defines_entry_1():
    import ast
    import builtins as _b

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    try:
        tree = ast.parse(sol)
    except SyntaxError as e:
        assert False, f"Solution code must parse without SyntaxError, got: {e}"

    assert tree is not None, "ast.parse should return an AST object for valid solution code."
    func_names = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    assert entry in func_names, f"Solution AST should define function '{entry}', found functions: {func_names}"


def test_exec_and_callable_entry_2():
    import builtins as _b

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    g = {"__builtins__": __builtins__}
    try:
        exec(sol, g)
    except Exception as e:
        assert False, f"Executing solution code should not raise an exception, got: {type(e).__name__}: {e}"

    assert entry in g, f"Executed module should define entry point '{entry}'."
    candidate = g[entry]
    assert callable(candidate), f"Entry point '{entry}' should be callable, got object of type {type(candidate).__name__}."


def test_signature_and_import_plausibility_3():
    import builtins as _b
    import inspect

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    g = {"__builtins__": __builtins__}
    try:
        exec(sol, g)
    except Exception as e:
        assert False, f"Solution code should execute successfully before signature inspection, got: {type(e).__name__}: {e}"

    assert entry in g, f"Expected entry point '{entry}' to exist after exec."
    candidate = g[entry]

    try:
        sig = inspect.signature(candidate)
    except Exception as e:
        assert False, f"Should be able to inspect signature of '{entry}', got: {type(e).__name__}: {e}"

    params = list(sig.parameters.values())
    assert len(params) == 0, f"Function '{entry}' should take no parameters, got signature {sig}."

    annotations = getattr(candidate, "__annotations__", {})
    if "return" in annotations:
        ret = annotations["return"]
        ret_name = getattr(ret, "__name__", str(ret))
        assert "QuantumCircuit" in ret_name or "qiskit.circuit" in str(ret), (
            f"If present, return annotation for '{entry}' should plausibly indicate QuantumCircuit, got {ret!r}."
        )