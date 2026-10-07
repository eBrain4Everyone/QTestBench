# SEMANTIC tests — Qiskit HumanEval task task_0035
# Generated: 2026-04-28T11:14:51.719639
# Model: anthropic/claude-opus-4-6 (claudeopus46)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from numpy import isclose\n    job = candidate()\n    assert isinstance(job, PrimitiveJob)\n    assert job.job_id() is not None\n    result = job.result()\n    assert isclose(result[0].data.evs.item(), 0.33, atol=0.06)\n'
ENTRY_POINT_NAME = 'run_circuit_with_dd_trex'
# --- Official check block end ---
import pytest

def test_return_type_1():
    """Test that the function returns a PrimitiveJob instance."""
    import builtins as _b
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


def test_job_result_structure_2():
    """Test that the job result has the expected structure with one expectation value."""
    import builtins as _b
    import numpy as np
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    job = candidate()
    result = job.result()

    # The result should have at least one PubResult
    assert len(result) >= 1, (
        f"Expected at least 1 pub result, got {len(result)}"
    )

    # Each pub result should have data with evs (expectation values)
    pub_result = result[0]
    evs = pub_result.data.evs
    assert evs is not None, "Expected expectation values (evs) in the result data"

    # The expectation value should be a real number in [-1, 1] for a single Pauli Z observable
    evs_val = float(evs)
    assert -1.0 <= evs_val <= 1.0 + 1e-6, (
        f"Expectation value {evs_val} out of expected range [-1, 1] for Z observable"
    )


def test_result_consistency_3():
    """Test that calling the function twice with same setup gives consistent results (deterministic seed)."""
    import builtins as _b
    import numpy as np
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    job1 = candidate()
    result1 = job1.result()
    evs1 = float(result1[0].data.evs)

    job2 = candidate()
    result2 = job2.result()
    evs2 = float(result2[0].data.evs)

    # With fixed seeds and fake backend, results should be reproducible
    assert np.allclose(evs1, evs2, atol=1e-4, rtol=1e-5), (
        f"Results not consistent across runs: {evs1} vs {evs2}. "
        "Expected deterministic behavior with fixed transpiler seed."
    )