# SEMANTIC tests — Qiskit HumanEval task task_0034
# Generated: 2026-04-28T12:05:37.755872
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
    assert isinstance(res, dict), "Result must be a dictionary"
    
    expected_keys = {'phi_plus', 'phi_minus', 'psi_plus', 'psi_minus'}
    assert expected_keys.issubset(res.keys()), f"Result must contain Bell state keys {expected_keys}"
    
    # Check for batch_id presence or tuple packaging
    if 'batch_id' in res:
        assert isinstance(res['batch_id'], str) or res['batch_id'] is None, "batch_id must be a string or None"
    else:
        for k in expected_keys:
            val = res[k]
            assert isinstance(val, tuple) and len(val) == 2, "If 'batch_id' is missing as a key, values must be tuples of (job, batch_id)"


def test_job_properties_2():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    res = candidate()
    bell_keys = ['phi_plus', 'phi_minus', 'psi_plus', 'psi_minus']
    
    for k in bell_keys:
        job = res[k]
        if isinstance(job, tuple):
            job = job[0]
            
        assert hasattr(job, 'job_id') or hasattr(job, 'result'), f"Value for {k} does not appear to be a valid job object"
        
        if hasattr(job, 'job_id') and callable(job.job_id):
            jid = job.job_id()
            assert isinstance(jid, str) or jid is None, f"Job ID for {k} is invalid"
        elif hasattr(job, 'job_id'):
            jid = job.job_id
            assert isinstance(jid, str) or jid is None, f"Job ID for {k} is invalid"


def test_job_execution_3():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    res = candidate()
    bell_keys = ['phi_plus', 'phi_minus', 'psi_plus', 'psi_minus']
    
    for k in bell_keys:
        job = res[k]
        if isinstance(job, tuple):
            job = job[0]
            
        try:
            # Calling result() ensures the job was successfully submitted and completed.
            # It also implicitly verifies that measurements were added to the circuits,
            # as SamplerV2 will fail otherwise.
            result = job.result()
            
            # SamplerV2 returns PrimitiveResult (has __len__), SamplerV1 returns SamplerResult (has quasi_dists)
            is_valid = hasattr(result, '__len__') or hasattr(result, 'quasi_dists') or hasattr(result, 'metadata')
            assert is_valid, f"Job result for {k} has an unexpected format or is invalid."
            
        except Exception as e:
            raise AssertionError(f"Failed to retrieve valid result for {k}: {e}")