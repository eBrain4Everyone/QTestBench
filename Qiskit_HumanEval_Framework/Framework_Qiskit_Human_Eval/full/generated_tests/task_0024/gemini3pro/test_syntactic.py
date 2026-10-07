# SYNTACTIC tests — Qiskit HumanEval task task_0024
# Generated: 2026-04-28T12:02:40.504987
# Model: google/gemini-3.1-pro-preview (gemini3pro)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    balanced = QuantumCircuit(5)\n    balanced.cx(3, 4)\n    assert candidate(balanced) == False\n    constant = QuantumCircuit(9)\n    constant.x(8)\n    assert candidate(constant) == True\n'
ENTRY_POINT_NAME = 'dj_algorithm'
# --- Official check block end ---
def test_module_load_and_callable_1():
    import builtins as _b
    import ast

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    try:
        ast.parse(sol)
    except SyntaxError as e:
        assert False, f"SyntaxError in candidate code: {e}"

    g = {"__builtins__": __builtins__}
    exec(sol, g)

    assert entry in g, f"Entry point '{entry}' not found in the module namespace."
    assert callable(g[entry]), f"Entry point '{entry}' is not callable."

def test_signature_2():
    import builtins as _b
    import inspect

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    sig = inspect.signature(candidate)
    params = list(sig.parameters.values())

    assert len(params) == 1, f"Function should take exactly 1 parameter, but found {len(params)}."
    
    if sig.return_annotation is not inspect.Signature.empty:
        assert sig.return_annotation in (bool, 'bool'), \
            f"Return type hint should be bool, got {sig.return_annotation}."

def test_basic_execution_3():
    import builtins as _b
    import numpy as np
    from qiskit import QuantumCircuit

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    # Minimal constant oracle: 2 qubits, empty circuit (f(x) = 0)
    # Qubit 0 is input, qubit 1 is output
    oracle = QuantumCircuit(2)

    try:
        result = candidate(oracle)
    except Exception as e:
        assert False, f"Execution failed on a minimal 2-qubit constant oracle: {e}"

    assert isinstance(result, (bool, np.bool_)), \
        f"Expected the algorithm to return a bool, but got {type(result)}."