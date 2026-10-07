# SYNTACTIC tests — Qiskit HumanEval task task_0035
# Generated: 2026-04-28T11:30:45.626942
# Model: deepseek/deepseek-v3.2 (deepseekv32)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from numpy import isclose\n    job = candidate()\n    assert isinstance(job, PrimitiveJob)\n    assert job.job_id() is not None\n    result = job.result()\n    assert isclose(result[0].data.evs.item(), 0.33, atol=0.06)\n'
ENTRY_POINT_NAME = 'run_circuit_with_dd_trex'
# --- Official check block end ---
import builtins as _b
import ast
import inspect
import sys

def test_entry_point_exists_1():
    """Check that the solution code can be parsed and executed, and the entry point exists."""
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    # parse syntax
    ast.parse(sol)
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    assert entry in g, f"Entry point '{entry}' not found in module namespace."
    candidate = g[entry]
    assert callable(candidate), f"'{entry}' is not callable."
    # optional: check it's a function
    assert inspect.isfunction(candidate), f"'{entry}' is not a function."

def test_signature_and_return_type_annotation_2():
    """Verify the function signature matches the problem statement (no arguments, returns PrimitiveJob)."""
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    sig = inspect.signature(candidate)
    # no parameters
    assert len(sig.parameters) == 0, f"Function should take no parameters, got {len(sig.parameters)}."
    # return annotation should be PrimitiveJob (or at least mention it)
    ret_ann = sig.return_annotation
    # allow string annotation or direct class
    ret_str = str(ret_ann)
    assert "PrimitiveJob" in ret_str, f"Return annotation should include PrimitiveJob, got {ret_ann}."

def test_imports_and_module_structure_3():
    """Check that required imports are present in the solution source (lightweight)."""
    sol = _b.INJECTED_SOLUTION_CODE
    # ensure no syntax errors
    ast.parse(sol)
    # verify that key names from the prompt are likely defined (not exhaustive)
    required_keywords = ["efficient_su2", "SparsePauliOp", "CouplingMap", "Estimator", "EstimatorOptions", "PrimitiveJob", "FakeAuckland", "generate_preset_pass_manager"]
    # just check they appear as substrings (crude but safe for syntactic test)
    for kw in required_keywords:
        assert kw in sol, f"Expected keyword '{kw}' not found in solution source."
    # also check the function definition is present
    entry = _b.INJECTED_ENTRY_POINT
    assert f"def {entry}" in sol, f"Function definition for '{entry}' not found in source."