# SYNTACTIC tests — Qiskit HumanEval task task_0035
# Generated: 2026-04-28T12:07:06.588050
# Model: google/gemini-3.1-pro-preview (gemini3pro)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from numpy import isclose\n    job = candidate()\n    assert isinstance(job, PrimitiveJob)\n    assert job.job_id() is not None\n    result = job.result()\n    assert isclose(result[0].data.evs.item(), 0.33, atol=0.06)\n'
ENTRY_POINT_NAME = 'run_circuit_with_dd_trex'
# --- Official check block end ---
def test_parse_and_exec_1():
    import builtins as _b
    import ast
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    try:
        ast.parse(sol)
    except SyntaxError as e:
        assert False, f"Code failed to parse: {e}"

    g = {"__builtins__": __builtins__}
    try:
        exec(sol, g)
    except Exception as e:
        assert False, f"Code failed to execute: {e}"

    assert entry in g, f"Entry point {entry} not found in executed namespace"

def test_callable_and_signature_2():
    import builtins as _b
    import inspect
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    g = {"__builtins__": __builtins__}
    exec(sol, g)

    func = g[entry]
    assert callable(func), f"Entry point {entry} is not callable"

    sig = inspect.signature(func)
    assert len(sig.parameters) == 0, f"Expected 0 arguments, got {len(sig.parameters)}"

def test_ast_structure_3():
    import builtins as _b
    import ast
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    tree = ast.parse(sol)
    func_nodes = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name == entry]
    
    assert len(func_nodes) >= 1, f"Could not find AST FunctionDef for {entry}."
    func_node = func_nodes[0]
    
    assert not func_node.args.args, "Function should not have positional arguments."
    assert not func_node.args.kwonlyargs, "Function should not have keyword arguments."
    assert not func_node.args.vararg, "Function should not have *args."
    assert not func_node.args.kwarg, "Function should not have **kwargs."