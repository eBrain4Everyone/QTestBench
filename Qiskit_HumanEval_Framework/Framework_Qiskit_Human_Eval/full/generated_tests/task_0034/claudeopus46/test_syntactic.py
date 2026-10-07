# SYNTACTIC tests — Qiskit HumanEval task task_0034
# Generated: 2026-04-28T11:13:49.436867
# Model: anthropic/claude-opus-4-6 (claudeopus46)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = "def check(candidate):\n    from numpy import isclose\n    jobs = candidate()\n    reference_data = {\n        'phi_plus': {'00': 0.10, '11': 0.10},\n        'phi_minus': {'00': 0.10, '11': 0.10},\n        'psi_plus': {'01': 0.10, '10': 0.10},\n        'psi_minus': {'01': 0.1, '10': 0.10}\n    }\n    assert isinstance(jobs, dict)\n    assert set(jobs.keys()) == set(reference_data.keys())\n    for state, job in jobs.items():\n        assert isinstance(job, PrimitiveJob)\n        assert job.job_id() is not None\n        counts = job.result()[0].data.meas.get_counts()\n        shots = 4096\n        normalized_counts = {k: v/shots for k, v in counts.items()}\n        for key, value in reference_data[state].items():\n            assert isclose(normalized_counts[key], value, atol=1e-01)\n"
ENTRY_POINT_NAME = 'run_jobs_on_batch'
# --- Official check block end ---
import ast
import inspect


def test_module_parses_and_loads_1():
    """Test that the solution source parses as valid Python and can be exec'd."""
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    # Check that the source is valid Python syntax
    tree = ast.parse(sol)
    assert tree is not None, "ast.parse returned None; source should be valid Python"

    # Check that exec succeeds without error
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    assert entry in g, f"Entry point '{entry}' not found in executed module namespace"


def test_entry_point_exists_and_callable_2():
    """Test that the entry point exists, is callable, and has the correct signature (no parameters)."""
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    g = {"__builtins__": __builtins__}
    exec(sol, g)

    candidate = g[entry]
    assert callable(candidate), f"'{entry}' should be callable but is {type(candidate)}"

    sig = inspect.signature(candidate)
    params = [
        p for p in sig.parameters.values()
        if p.default is inspect.Parameter.empty
        and p.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
    ]
    assert len(params) == 0, (
        f"'{entry}' should take no required arguments, but has required params: {params}"
    )


def test_return_annotation_and_module_structure_3():
    """Test that the module contains expected imports and the function has a dict return annotation."""
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    # Parse AST and look for the function definition
    tree = ast.parse(sol)
    func_defs = [
        node for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == entry
    ]
    assert len(func_defs) >= 1, f"Function '{entry}' not found in AST"

    # Check that the module references expected identifiers somewhere in source
    source_lower = sol.lower()
    assert "quantumcircuit" in source_lower or "qc" in source_lower, (
        "Solution should reference QuantumCircuit or build circuits"
    )
    assert "batch" in source_lower, (
        "Solution should reference Batch for batch mode execution"
    )
    assert "sampler" in source_lower, (
        "Solution should reference Sampler (SamplerV2)"
    )
    assert "fakealgiers" in source_lower or "fake_algiers" in source_lower, (
        "Solution should reference FakeAlgiers backend"
    )

    # Verify the function is loadable and the return annotation (if present) is dict
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    sig = inspect.signature(candidate)
    if sig.return_annotation is not inspect.Parameter.empty:
        assert sig.return_annotation is dict or sig.return_annotation == "dict", (
            f"Return annotation should be dict, got {sig.return_annotation}"
        )