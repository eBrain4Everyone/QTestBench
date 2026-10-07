# SYNTACTIC tests — Qiskit HumanEval task task_0003
# Generated: 2026-04-28T12:34:11.679972
# Model: openai/gpt-5.4 (gpt54)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from qiskit.quantum_info import Statevector\n    import math\n    import matplotlib\n\n    def check_circuit(circuit):\n        assert circuit.data[-1].operation.name == "measure"\n        circuit.remove_final_measurements()\n        ghz_statevector = (\n            Statevector.from_label("000") + Statevector.from_label("111")\n        ) / math.sqrt(2)\n        assert Statevector.from_instruction(circuit).equiv(ghz_statevector)\n\n    circuit = candidate()\n    check_circuit(circuit)\n\n    circuit, drawing = candidate(drawing=True)\n    check_circuit(circuit)\n    assert isinstance(drawing, matplotlib.figure.Figure)\n'
ENTRY_POINT_NAME = 'create_ghz'
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
        raise AssertionError(f"Executing solution source should succeed without import/runtime errors, got: {e}") from e

    assert entry in g, f"Executed module must define the entry point '{entry}'."
    assert callable(g[entry]), f"Entry point '{entry}' must be callable."


def test_signature_plausibility_2():
    import builtins as _b
    import inspect

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    g = {"__builtins__": __builtins__}
    try:
        exec(sol, g)
    except Exception as e:
        raise AssertionError(f"Executing solution source should succeed before signature inspection, got: {e}") from e

    assert entry in g, f"Executed module must contain '{entry}' for signature inspection."
    candidate = g[entry]
    assert callable(candidate), f"'{entry}' must be callable to inspect its signature."

    try:
        sig = inspect.signature(candidate)
    except Exception as e:
        raise AssertionError(f"inspect.signature should work on '{entry}', got: {e}") from e

    params = list(sig.parameters.values())
    assert len(params) <= 1, "create_ghz should not require more than one parameter."
    if len(params) == 1:
        p = params[0]
        assert p.name == "drawing", "If a parameter is present, it should be named 'drawing'."
        assert p.default is not inspect._empty, "The 'drawing' parameter should be optional with a default value."


def test_interface_and_docstring_plausibility_3():
    import builtins as _b
    import inspect

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    g = {"__builtins__": __builtins__}
    try:
        exec(sol, g)
    except Exception as e:
        raise AssertionError(f"Solution source must execute successfully for interface checks, got: {e}") from e

    assert "create_ghz" in g, "Module should define a function named 'create_ghz' as described in the prompt."
    assert entry == "create_ghz", f"Injected entry point should be 'create_ghz' for this task, got '{entry}'."

    candidate = g[entry]
    assert inspect.isfunction(candidate) or callable(candidate), "Entry point should be a function or otherwise callable."

    doc = inspect.getdoc(candidate)
    assert doc is None or isinstance(doc, str), "Docstring, if present, should be a string."
    if doc:
        lowered = doc.lower()
        assert "ghz" in lowered, "Docstring should plausibly mention GHZ when present."
        assert "measure" in lowered or "circuit" in lowered, "Docstring should plausibly describe returning or measuring a circuit."