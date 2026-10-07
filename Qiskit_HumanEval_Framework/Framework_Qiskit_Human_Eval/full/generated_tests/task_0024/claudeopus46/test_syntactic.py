# SYNTACTIC tests — Qiskit HumanEval task task_0024
# Generated: 2026-04-28T11:13:03.242056
# Model: anthropic/claude-opus-4-6 (claudeopus46)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    balanced = QuantumCircuit(5)\n    balanced.cx(3, 4)\n    assert candidate(balanced) == False\n    constant = QuantumCircuit(9)\n    constant.x(8)\n    assert candidate(constant) == True\n'
ENTRY_POINT_NAME = 'dj_algorithm'
# --- Official check block end ---
def test_module_loads_and_parses_1():
    """Test that the solution source code is valid Python and can be parsed."""
    import ast
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    # Should parse without SyntaxError
    tree = ast.parse(sol)
    assert tree is not None, "ast.parse returned None; source code is invalid Python"
    assert isinstance(tree, ast.Module), "Parsed AST should be a Module node"


def test_entry_point_exists_and_callable_2():
    """Test that exec(sol) succeeds and the entry point is a callable function."""
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    assert entry == "dj_algorithm", f"Expected entry point 'dj_algorithm', got '{entry}'"
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    assert entry in g, f"Entry point '{entry}' not found in executed module namespace"
    candidate = g[entry]
    assert callable(candidate), f"Entry point '{entry}' is not callable"


def test_signature_accepts_quantum_circuit_3():
    """Test that the function signature accepts a single positional argument (the oracle)."""
    import inspect
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    sig = inspect.signature(candidate)
    params = list(sig.parameters.values())
    # Should have at least one parameter for the oracle
    assert len(params) >= 1, (
        f"Expected at least 1 parameter (oracle), got {len(params)} parameters"
    )
    # The first parameter should accept a positional argument
    first_param = params[0]
    assert first_param.kind in (
        inspect.Parameter.POSITIONAL_ONLY,
        inspect.Parameter.POSITIONAL_OR_KEYWORD,
    ), f"First parameter '{first_param.name}' should accept positional argument, kind={first_param.kind}"
    # Verify the parameter name is reasonable (oracle or similar)
    assert first_param.name == "oracle", (
        f"Expected first parameter named 'oracle', got '{first_param.name}'"
    )