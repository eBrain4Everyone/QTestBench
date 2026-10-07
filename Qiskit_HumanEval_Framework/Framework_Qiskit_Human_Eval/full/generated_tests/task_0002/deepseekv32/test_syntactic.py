# SYNTACTIC tests — Qiskit HumanEval task task_0002
# Generated: 2026-04-28T11:19:37.902333
# Model: deepseek/deepseek-v3.2 (deepseekv32)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    solution = (Statevector.from_label("00") + Statevector.from_label("11")) / sqrt(2)\n    assert result.equiv(solution)\n'
ENTRY_POINT_NAME = 'create_bell_statevector'
# --- Official check block end ---
import builtins as _b
import ast
import inspect
import pytest

def test_module_imports_and_parses_1():
    """Check that the solution code is valid Python and loads."""
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    # parse must not raise
    ast.parse(sol)
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    assert entry in g, f"Entry point '{entry}' not found in namespace"
    assert callable(g[entry]), f"Entry point '{entry}' is not callable"
    # optional: verify it's named create_bell_statevector as per problem
    assert entry == "create_bell_statevector", f"Expected entry 'create_bell_statevector', got '{entry}'"

def test_signature_and_return_type_hint_2():
    """Check the signature matches the expected form."""
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    sig = inspect.signature(candidate)
    # should take no parameters (except self if bound method, but free function)
    assert len(sig.parameters) == 0, f"Expected zero parameters, got {len(sig.parameters)}"
    # return annotation hint should be Statevector (optional check)
    ret_ann = sig.return_annotation
    # allow Statevector or inspect.Signature.empty (no annotation)
    if ret_ann is not inspect.Signature.empty:
        # check string or class
        if isinstance(ret_ann, str):
            assert ret_ann == "Statevector", f"Return annotation string mismatch: {ret_ann}"
        else:
            # could be imported Statevector type
            from qiskit.quantum_info import Statevector
            assert ret_ann is Statevector, f"Return annotation type mismatch: {ret_ann}"

def test_basic_call_and_statevector_instance_3():
    """Check that calling returns a Statevector with correct dimension."""
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    result = candidate()   # must not raise
    from qiskit.quantum_info import Statevector
    assert isinstance(result, Statevector), f"Result is not a Statevector: {type(result)}"
    # Bell state is 2_qubit statevector, dimension 4
    assert result.dim == 4, f"Expected dimension 4, got {result.dim}"
    # quick plausibility: norm should be 1
    import numpy as np
    assert np.allclose(result.inner(result).real, 1.0, atol=1e-10), "Statevector norm is not 1"