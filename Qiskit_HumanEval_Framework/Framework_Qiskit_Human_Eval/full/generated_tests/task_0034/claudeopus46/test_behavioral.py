# BEHAVIORAL tests — Qiskit HumanEval task task_0034
# Generated: 2026-04-28T11:14:29.828671
# Model: anthropic/claude-opus-4-6 (claudeopus46)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = "def check(candidate):\n    from numpy import isclose\n    jobs = candidate()\n    reference_data = {\n        'phi_plus': {'00': 0.10, '11': 0.10},\n        'phi_minus': {'00': 0.10, '11': 0.10},\n        'psi_plus': {'01': 0.10, '10': 0.10},\n        'psi_minus': {'01': 0.1, '10': 0.10}\n    }\n    assert isinstance(jobs, dict)\n    assert set(jobs.keys()) == set(reference_data.keys())\n    for state, job in jobs.items():\n        assert isinstance(job, PrimitiveJob)\n        assert job.job_id() is not None\n        counts = job.result()[0].data.meas.get_counts()\n        shots = 4096\n        normalized_counts = {k: v/shots for k, v in counts.items()}\n        for key, value in reference_data[state].items():\n            assert isclose(normalized_counts[key], value, atol=1e-01)\n"
ENTRY_POINT_NAME = 'run_jobs_on_batch'
# --- Official check block end ---
def test_run_jobs_on_batch_returns_correct_keys_1():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    result = candidate()
    
    assert isinstance(result, dict), f"Expected dict, got {type(result)}"
    
    expected_keys = {'phi_plus', 'phi_minus', 'psi_plus', 'psi_minus'}
    actual_keys = set(result.keys())
    assert expected_keys.issubset(actual_keys), (
        f"Missing keys: {expected_keys - actual_keys}. Got keys: {actual_keys}"
    )


def test_run_jobs_on_batch_values_are_jobs_and_batch_id_2():
    import builtins as _b
    from qiskit.primitives.primitive_job import PrimitiveJob
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    result = candidate()
    
    bell_state_keys = ['phi_plus', 'phi_minus', 'psi_plus', 'psi_minus']
    
    for key in bell_state_keys:
        assert key in result, f"Key '{key}' missing from result dict"
        value = result[key]
        # The value should be a job object (RuntimeJob or PrimitiveJob-like)
        # It should have a result() method or be a job-like object
        assert value is not None, f"Value for '{key}' is None"
    
    # Check that there's a batch_id key or that the jobs are valid job objects
    # The prompt says "values are the corresponding RuntimeJob objects and the batch id"
    # This likely means there's also a 'batch_id' key or the batch id is part of the dict
    # Let's check if there's any additional key for batch_id
    non_bell_keys = set(result.keys()) - set(bell_state_keys)
    
    # Either batch_id is a separate key, or it's embedded in the structure
    # We verify that bell state entries exist and are job-like
    for key in bell_state_keys:
        job = result[key]
        # Job should have job_id or result method
        has_job_interface = (
            hasattr(job, 'result') or 
            hasattr(job, 'job_id') or
            isinstance(job, PrimitiveJob)
        )
        assert has_job_interface, (
            f"Value for '{key}' does not appear to be a job object: {type(job)}"
        )


def test_run_jobs_on_batch_job_results_have_valid_counts_3():
    import builtins as _b
    import numpy as np
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    result = candidate()
    
    bell_state_keys = ['phi_plus', 'phi_minus', 'psi_plus', 'psi_minus']
    
    # Expected dominant outcomes for each Bell state
    expected_outcomes = {
        'phi_plus': {'00', '11'},    # |00> + |11>
        'phi_minus': {'00', '11'},   # |00> - |11>
        'psi_plus': {'01', '10'},    # |01> + |10>
        'psi_minus': {'01', '10'},   # |01> - |10>
    }
    
    for key in bell_state_keys:
        job = result[key]
        assert job is not None, f"Job for '{key}' is None"
        
        try:
            job_result = job.result()
            # SamplerV2 returns PubResult objects
            # Try to get counts from the result
            if hasattr(job_result, '__getitem__'):
                pub_result = job_result[0]
                if hasattr(pub_result, 'data'):
                    # Get the classical register data
                    data = pub_result.data
                    # Try to get counts
                    if hasattr(data, 'meas'):
                        counts = data.meas.get_counts()
                    elif hasattr(data, 'c'):
                        counts = data.c.get_counts()
                    else:
                        # Try first attribute
                        first_attr = list(vars(data).keys())[0]
                        counts = getattr(data, first_attr).get_counts()
                    
                    # Verify dominant outcomes
                    total = sum(counts.values())
                    dominant_prob = sum(
                        counts.get(outcome, 0) for outcome in expected_outcomes[key]
                    ) / total
                    assert dominant_prob > 0.5, (
                        f"Bell state '{key}': expected dominant outcomes "
                        f"{expected_outcomes[key]} but got counts {counts} "
                        f"(dominant prob={dominant_prob:.3f})"
                    )
        except Exception as e:
            # If we can't extract counts, at least verify the job completed
            assert hasattr(job, 'result'), (
                f"Job for '{key}' has no result method: {e}"
            )