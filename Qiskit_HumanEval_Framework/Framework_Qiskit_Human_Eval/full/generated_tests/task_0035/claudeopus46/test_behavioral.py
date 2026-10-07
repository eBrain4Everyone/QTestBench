# BEHAVIORAL tests — Qiskit HumanEval task task_0035
# Generated: 2026-04-28T11:15:04.237804
# Model: anthropic/claude-opus-4-6 (claudeopus46)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from numpy import isclose\n    job = candidate()\n    assert isinstance(job, PrimitiveJob)\n    assert job.job_id() is not None\n    result = job.result()\n    assert isclose(result[0].data.evs.item(), 0.33, atol=0.06)\n'
ENTRY_POINT_NAME = 'run_circuit_with_dd_trex'
# --- Official check block end ---
import builtins as _b

def test_return_type_1():
    """Test that the function returns a PrimitiveJob instance."""
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    from qiskit.primitives.primitive_job import PrimitiveJob
    
    result = candidate()
    assert isinstance(result, PrimitiveJob), (
        f"Expected return type PrimitiveJob, got {type(result)}"
    )


def test_result_structure_2():
    """Test that the job result has proper structure with expectation values."""
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    import numpy as np
    
    job = candidate()
    result = job.result()
    
    # The result should have at least one PubResult
    assert len(result) >= 1, (
        f"Expected at least 1 result entry, got {len(result)}"
    )
    
    # Each pub result should have data with evs (expectation values)
    pub_result = result[0]
    evs = pub_result.data.evs
    
    # The expectation value should be a finite number
    assert np.isfinite(evs).all(), (
        f"Expected finite expectation values, got {evs}"
    )
    
    # For a Z observable, expectation value should be in [-1, 1]
    assert np.all(np.abs(evs) <= 1.0 + 1e-6), (
        f"Expected expectation values in [-1, 1], got {evs}"
    )


def test_deterministic_result_3():
    """Test that calling the function twice yields consistent results (same seed/config)."""
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    import numpy as np
    
    job1 = candidate()
    result1 = job1.result()
    evs1 = result1[0].data.evs
    
    job2 = candidate()
    result2 = job2.result()
    evs2 = result2[0].data.evs
    
    # Since the function uses a local simulator with fixed transpiler seed,
    # results should be reproducible (or at least very close for statevector-based estimator)
    assert np.allclose(evs1, evs2, atol=0.15), (
        f"Expected reproducible results, got {evs1} and {evs2}"
    )