# SYNTACTIC tests — Qiskit HumanEval task task_0034
# Generated: 2026-04-28T11:28:11.243894
# Model: deepseek/deepseek-v3.2 (deepseekv32)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = "def check(candidate):\n    from numpy import isclose\n    jobs = candidate()\n    reference_data = {\n        'phi_plus': {'00': 0.10, '11': 0.10},\n        'phi_minus': {'00': 0.10, '11': 0.10},\n        'psi_plus': {'01': 0.10, '10': 0.10},\n        'psi_minus': {'01': 0.1, '10': 0.10}\n    }\n    assert isinstance(jobs, dict)\n    assert set(jobs.keys()) == set(reference_data.keys())\n    for state, job in jobs.items():\n        assert isinstance(job, PrimitiveJob)\n        assert job.job_id() is not None\n        counts = job.result()[0].data.meas.get_counts()\n        shots = 4096\n        normalized_counts = {k: v/shots for k, v in counts.items()}\n        for key, value in reference_data[state].items():\n            assert isclose(normalized_counts[key], value, atol=1e-01)\n"
ENTRY_POINT_NAME = 'run_jobs_on_batch'
# --- Official check block end ---
import builtins as _b
import sys
import ast
import inspect

sol = _b.INJECTED_SOLUTION_CODE
entry = _b.INJECTED_ENTRY_POINT

def test_syntactic_validity_1():
    """Check that the solution code parses as valid Python."""
    try:
        ast.parse(sol)
    except SyntaxError as e:
        raise AssertionError(f"Solution code is not valid Python: {e}") from e
    assert True, "Solution code parses successfully"

def test_entry_point_exists_and_callable_2():
    """Check that the entry point function exists and is callable with no required arguments."""
    g = {"__builtins__": __builtins__}
    try:
        exec(sol, g)
    except Exception as e:
        raise AssertionError(f"Executing solution code raised an exception: {e}") from e
    assert entry in g, f"Entry point '{entry}' not found in module namespace"
    candidate = g[entry]
    assert callable(candidate), f"Entry point '{entry}' is not callable"
    # Check it can be called with zero arguments (as per problem statement)
    try:
        sig = inspect.signature(candidate)
        # No required parameters, or only optional ones
        required_params = [p for p in sig.parameters.values() if p.default == inspect.Parameter.empty]
        assert len(required_params) == 0, f"Entry point '{entry}' requires arguments: {required_params}"
    except Exception as e:
        raise AssertionError(f"Failed to inspect signature of '{entry}': {e}") from e
    assert True, f"Entry point '{entry}' exists, is callable, and takes no required arguments"

def test_return_type_annotation_and_docstring_3():
    """Check that the function has a return type annotation dict and a docstring as described."""
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    # Verify docstring exists and mentions Bell states
    doc = inspect.getdoc(candidate)
    assert doc is not None, f"Entry point '{entry}' must have a docstring"
    # Check for keywords from the prompt
    keywords = ["Bell", "phi_plus", "phi_minus", "psi_plus", "psi_minus", "batch", "FakeAlgiers", "Sampler"]
    found = [kw for kw in keywords if kw.lower() in doc.lower()]
    assert len(found) >= 2, f"Docstring should mention relevant concepts; found only {found}"
    # Check return type annotation
    sig = inspect.signature(candidate)
    return_annotation = sig.return_annotation
    # It should be dict (or a more specific annotation, but dict is required by prompt)
    # We'll accept any annotation that is or contains dict
    annotation_str = str(return_annotation)
    assert "dict" in annotation_str, f"Return annotation should include dict, got {return_annotation}"
    assert True, "Function has appropriate docstring and return annotation"