# SYNTACTIC tests — Qiskit HumanEval task task_0020
# Generated: 2026-04-28T11:25:04.236412
# Model: deepseek/deepseek-v3.2 (deepseekv32)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    result.remove_final_measurements()\n    backend = FakePerth()\n    assert result.num_qubits == backend.num_qubits\n    assert result.layout.initial_index_layout()[:3] == [2, 4, 6]\n'
ENTRY_POINT_NAME = 'transpile_ghz_customlayout'
# --- Official check block end ---
import builtins as _b
import ast
import inspect

def test_basic_imports_and_syntax_1():
    """Ensure the solution code is syntactically valid Python."""
    sol = _b.INJECTED_SOLUTION_CODE
    # parse the code; if it raises a SyntaxError, the test fails
    try:
        ast.parse(sol)
    except SyntaxError as e:
        raise AssertionError(f"Solution code is not valid Python: {e}")

def test_entry_point_exists_and_callable_2():
    """Check that the entry point exists and is a callable."""
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    namespace = {"__builtins__": __builtins__}
    exec(sol, namespace)
    # ensure entry point is present
    assert entry in namespace, f"Entry point '{entry}' not found in module namespace."
    candidate = namespace[entry]
    # ensure it's callable
    assert callable(candidate), f"'{entry}' is not callable."
    # optional: check it's a function (not a class etc.)
    assert isinstance(candidate, type(lambda: None)), f"'{entry}' is not a function."

def test_signature_and_return_type_hint_3():
    """Verify the function has correct name and no required arguments."""
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    namespace = {"__builtins__": __builtins__}
    exec(sol, namespace)
    candidate = namespace[entry]
    sig = inspect.signature(candidate)
    # function should take no arguments (except possibly self if method, but it's a function)
    assert len(sig.parameters) == 0, f"Function should have 0 parameters, got {len(sig.parameters)}."
    # check return annotation mentions QuantumCircuit (optional but good)
    if sig.return_annotation is not inspect.Signature.empty:
        # allow string annotation or actual type
        ret_ann = str(sig.return_annotation)
        assert "QuantumCircuit" in ret_ann, f"Return annotation should mention QuantumCircuit, got {ret_ann}"