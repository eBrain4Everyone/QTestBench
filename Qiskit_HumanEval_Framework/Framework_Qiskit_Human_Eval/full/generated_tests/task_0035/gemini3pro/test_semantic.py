# SEMANTIC tests — Qiskit HumanEval task task_0035
# Generated: 2026-04-28T12:07:57.347305
# Model: google/gemini-3.1-pro-preview (gemini3pro)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from numpy import isclose\n    job = candidate()\n    assert isinstance(job, PrimitiveJob)\n    assert job.job_id() is not None\n    result = job.result()\n    assert isclose(result[0].data.evs.item(), 0.33, atol=0.06)\n'
ENTRY_POINT_NAME = 'run_circuit_with_dd_trex'
# --- Official check block end ---
def test_returned_job_1():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    job = candidate()
    
    # Must return an object that behaves like a job
    assert hasattr(job, "result") and callable(job.result), "Returned object must have a callable result() method."
    assert hasattr(job, "job_id") and callable(job.job_id), "Returned object must have a callable job_id() method."


def test_job_execution_2():
    import builtins as _b
    import numpy as np
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    job = candidate()
    result = job.result()
    
    # Check that we can extract expectation values (supports both V1 and V2 interfaces)
    evs = None
    if hasattr(result, "values"):
        evs = result.values
    elif hasattr(result, "__len__") and hasattr(result[0], "data"):
        evs = result[0].data.evs
        
    assert evs is not None, "Could not extract expectation values from job result. Ensure an Estimator is used."
    
    evs_arr = np.atleast_1d(evs)
    assert len(evs_arr) >= 1, "Result must contain at least one expectation value."


def test_observable_bounds_3():
    import builtins as _b
    import numpy as np
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    job = candidate()
    result = job.result()
    
    if hasattr(result, "values"):
        evs = result.values
    else:
        evs = result[0].data.evs
        
    ev = np.atleast_1d(evs)[0]
    
    # Expectation value for a Pauli observable must be in [-1, 1].
    # We allow some noise margin up to 1.2 to account for statistical fluctuations or mitigation artifacts.
    assert -1.2 <= ev <= 1.2, f"Expectation value {ev} out of valid bounds [-1, 1] plus noise margin."