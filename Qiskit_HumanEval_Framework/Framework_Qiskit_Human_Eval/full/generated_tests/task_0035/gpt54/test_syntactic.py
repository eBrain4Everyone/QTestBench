# SYNTACTIC tests — Qiskit HumanEval task task_0035
# Generated: 2026-04-28T12:37:34.879975
# Model: openai/gpt-5.4 (gpt54)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from numpy import isclose\n    job = candidate()\n    assert isinstance(job, PrimitiveJob)\n    assert job.job_id() is not None\n    result = job.result()\n    assert isclose(result[0].data.evs.item(), 0.33, atol=0.06)\n'
ENTRY_POINT_NAME = 'run_circuit_with_dd_trex'
# --- Official check block end ---
def test_module_parses_and_entry_exists_1():
    import ast
    import builtins as _b

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    try:
        tree = ast.parse(sol)
    except SyntaxError as e:
        raise AssertionError(f"Solution source must be valid Python syntax, but ast.parse failed: {e}") from e

    assert tree is not None, "Parsed AST should not be None for valid solution source."

    g = {"__builtins__": __builtins__}
    try:
        exec(sol, g)
    except Exception as e:
        raise AssertionError(f"Executing solution source should succeed, but exec failed: {type(e).__name__}: {e}") from e

    assert entry in g, f"Entry point '{entry}' must exist in executed globals."
    assert callable(g[entry]), f"Entry point '{entry}' must be callable."


def test_entry_signature_no_required_args_2():
    import builtins as _b
    import inspect

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    assert callable(candidate), f"Resolved entry point '{entry}' must be callable."

    sig = inspect.signature(candidate)
    params = list(sig.parameters.values())

    required = [
        p for p in params
        if p.default is inspect._empty
        and p.kind in (inspect.Parameter.POSITIONAL_ONLY,
                       inspect.Parameter.POSITIONAL_OR_KEYWORD,
                       inspect.Parameter.KEYWORD_ONLY)
    ]

    assert len(required) == 0, (
        f"Function '{entry}' should be callable without required arguments, "
        f"but found required parameters: {[p.name for p in required]}"
    )


def test_source_mentions_expected_qiskit_context_3():
    import builtins as _b

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    g = {"__builtins__": __builtins__}
    exec(sol, g)

    assert entry in g and callable(g[entry]), f"Entry point '{entry}' must be defined and callable after exec."

    normalized = sol.replace('"', "'")

    assert "def run_circuit_with_dd_trex" in normalized, (
        "Solution source should define the expected function name 'run_circuit_with_dd_trex'."
    )
    assert ("efficient_su2" in normalized or "EfficientSU2" in normalized), (
        "Solution source should plausibly reference an EfficientSU2 circuit construction."
    )
    assert "FakeAuckland" in normalized, (
        "Solution source should plausibly reference the FakeAuckland backend required by the prompt."
    )
    assert ("Estimator" in normalized or "PrimitiveJob" in normalized), (
        "Solution source should plausibly reference estimator/job APIs consistent with the task."
    )