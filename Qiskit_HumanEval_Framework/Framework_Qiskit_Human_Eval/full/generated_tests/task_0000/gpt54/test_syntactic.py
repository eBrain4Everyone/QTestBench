# SYNTACTIC tests — Qiskit HumanEval task task_0000
# Generated: 2026-04-28T12:26:23.357094
# Model: openai/gpt-5.4 (gpt54)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate(3)\n    assert isinstance(result, QuantumCircuit)\n    assert result.num_qubits == 3\n'
ENTRY_POINT_NAME = 'create_quantum_circuit'
# --- Official check block end ---
def test_module_loads_and_entry_exists_1():
    import ast
    import builtins as _b

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    try:
        tree = ast.parse(sol)
    except SyntaxError as e:
        assert False, f"Solution source must be valid Python syntax, but ast.parse failed: {e}"

    assert tree is not None, "ast.parse should return an AST object for valid solution source."

    g = {"__builtins__": __builtins__}
    try:
        exec(sol, g)
    except Exception as e:
        assert False, f"Executing the solution source should not raise an exception, but got: {e}"

    assert entry in g, f"Entry point '{entry}' must exist in the executed solution namespace."
    assert callable(g[entry]), f"Entry point '{entry}' must be callable after executing the solution."


def test_signature_and_name_2():
    import builtins as _b
    import inspect

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    assert callable(candidate), f"Resolved entry point '{entry}' must be callable."
    assert candidate.__name__ == entry, f"Callable name should match entry point '{entry}'."

    sig = inspect.signature(candidate)
    params = list(sig.parameters.values())

    assert len(params) == 1, "create_quantum_circuit should accept exactly one parameter."
    assert params[0].kind in (
        inspect.Parameter.POSITIONAL_ONLY,
        inspect.Parameter.POSITIONAL_OR_KEYWORD,
    ), "The single parameter should be positional or positional-or-keyword."
    assert params[0].name == "n_qubits", "The function parameter should be named 'n_qubits' as specified."


def test_basic_return_plausibility_3():
    import builtins as _b

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    try:
        result = candidate(1)
    except Exception as e:
        assert False, f"Calling the candidate with a basic integer input should not fail, but got: {e}"

    try:
        from qiskit import QuantumCircuit
    except Exception as e:
        assert False, f"Qiskit QuantumCircuit should be importable for this task, but import failed: {e}"

    assert isinstance(result, QuantumCircuit), "create_quantum_circuit(1) should return a qiskit.QuantumCircuit instance."
    assert hasattr(result, "num_qubits"), "Returned object should expose 'num_qubits' like a QuantumCircuit."
    assert result.num_qubits == 1, "Returned circuit for input 1 should have exactly 1 qubit."