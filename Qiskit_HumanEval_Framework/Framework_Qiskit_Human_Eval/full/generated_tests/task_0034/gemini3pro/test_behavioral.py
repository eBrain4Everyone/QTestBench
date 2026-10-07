# BEHAVIORAL tests — Qiskit HumanEval task task_0034
# Generated: 2026-04-28T12:06:38.026997
# Model: google/gemini-3.1-pro-preview (gemini3pro)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = "def check(candidate):\n    from numpy import isclose\n    jobs = candidate()\n    reference_data = {\n        'phi_plus': {'00': 0.10, '11': 0.10},\n        'phi_minus': {'00': 0.10, '11': 0.10},\n        'psi_plus': {'01': 0.10, '10': 0.10},\n        'psi_minus': {'01': 0.1, '10': 0.10}\n    }\n    assert isinstance(jobs, dict)\n    assert set(jobs.keys()) == set(reference_data.keys())\n    for state, job in jobs.items():\n        assert isinstance(job, PrimitiveJob)\n        assert job.job_id() is not None\n        counts = job.result()[0].data.meas.get_counts()\n        shots = 4096\n        normalized_counts = {k: v/shots for k, v in counts.items()}\n        for key, value in reference_data[state].items():\n            assert isclose(normalized_counts[key], value, atol=1e-01)\n"
ENTRY_POINT_NAME = 'run_jobs_on_batch'
# --- Official check block end ---
def test_dictionary_structure_1():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    res = candidate()
    
    assert isinstance(res, dict), "Return value must be a dictionary."
    expected_keys = {'phi_plus', 'phi_minus', 'psi_plus', 'psi_minus', 'batch_id'}
    for k in expected_keys:
        assert k in res, f"Dictionary missing key: {k}"

def test_job_properties_2():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    res = candidate()
    
    assert res['batch_id'] is not None, "batch_id should not be None"
    
    for key in ['phi_plus', 'phi_minus', 'psi_plus', 'psi_minus']:
        job = res[key]
        assert hasattr(job, 'result'), f"Value for {key} should have a result() method."

def test_bell_state_results_3():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    res = candidate()
    
    job_phi_plus = res['phi_plus']
    result = job_phi_plus.result()
    
    has_counts = False
    
    if hasattr(result, 'quasi_dists'):
        dist = result.quasi_dists[0]
        assert 0 in dist and 3 in dist, "phi_plus should have support on '00' and '11' (0 and 3)"
        has_counts = True
    elif hasattr(result, '__getitem__') and hasattr(result[0], 'data'):
        pub_result = result[0]
        for key in dir(pub_result.data):
            if not key.startswith('_'):
                val = getattr(pub_result.data, key)
                if hasattr(val, 'get_counts'):
                    counts = val.get_counts()
                    found_00 = any(k.replace(' ', '') == '00' for k in counts.keys())
                    found_11 = any(k.replace(' ', '') == '11' for k in counts.keys())
                    assert found_00 and found_11, f"phi_plus should have support on 00 and 11, got {counts}"
                    has_counts = True
                    break
                
    assert has_counts, "Could not extract counts/quasi_dists from the job result."