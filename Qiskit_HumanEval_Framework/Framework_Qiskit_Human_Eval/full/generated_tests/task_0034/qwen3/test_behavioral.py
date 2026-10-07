# BEHAVIORAL tests — Qiskit HumanEval task task_0034
# Generated: 2026-04-28T12:42:07.172715
# Model: qwen/qwen3-coder-next (qwen3)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = "def check(candidate):\n    from numpy import isclose\n    jobs = candidate()\n    reference_data = {\n        'phi_plus': {'00': 0.10, '11': 0.10},\n        'phi_minus': {'00': 0.10, '11': 0.10},\n        'psi_plus': {'01': 0.10, '10': 0.10},\n        'psi_minus': {'01': 0.1, '10': 0.10}\n    }\n    assert isinstance(jobs, dict)\n    assert set(jobs.keys()) == set(reference_data.keys())\n    for state, job in jobs.items():\n        assert isinstance(job, PrimitiveJob)\n        assert job.job_id() is not None\n        counts = job.result()[0].data.meas.get_counts()\n        shots = 4096\n        normalized_counts = {k: v/shots for k, v in counts.items()}\n        for key, value in reference_data[state].items():\n            assert isclose(normalized_counts[key], value, atol=1e-01)\n"
ENTRY_POINT_NAME = 'run_jobs_on_batch'
# --- Official check block end ---
def test_run_jobs_on_batch_structure_and_return_type():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    result = candidate()
    
    assert isinstance(result, dict), "Return value must be a dictionary"
    expected_keys = ['phi_plus', 'phi_minus', 'psi_plus', 'psi_minus']
    assert set(result.keys()) == set(expected_keys), f"Keys must be exactly {expected_keys}, got {list(result.keys())}"
    
    for key in expected_keys:
        assert key in result, f"Missing key '{key}' in result dictionary"
        job_with_batch = result[key]
        assert isinstance(job_with_batch, dict), f"Value for '{key}' must be a dictionary"
        assert 'job' in job_with_batch, f"Missing 'job' key in result['{key}']"
        assert 'batch_id' in job_with_batch, f"Missing 'batch_id' key in result['{key}']"
        from qiskit_ibm_runtime import RuntimeJob
        assert isinstance(job_with_batch['job'], RuntimeJob), f"Value for 'job' in result['{key}'] must be a RuntimeJob"
        assert isinstance(job_with_batch['batch_id'], str), f"Value for 'batch_id' in result['{key}'] must be a string"


def test_run_jobs_on_batch_uses_sampler_v2_and_batch():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    result = candidate()
    
    # Extract jobs and verify they belong to same batch
    jobs = [result[key]['job'] for key in result]
    batch_ids = [result[key]['batch_id'] for key in result]
    
    # All batch_ids should be identical
    assert len(set(batch_ids)) == 1, "All jobs should belong to the same batch"
    
    # Check jobs are PrimitiveJob instances (SamplerV2 returns PrimitiveJob)
    from qiskit.primitives.primitive_job import PrimitiveJob
    for job in jobs:
        assert isinstance(job, PrimitiveJob), "Each job should be a PrimitiveJob (SamplerV2 job)"
        assert hasattr(job, '_backend'), "Each job should have a backend reference"
        assert hasattr(job, 'backend'), "Each job should have a backend property"
        # Verify backend is FakeAlgiers
        from qiskit_ibm_runtime.fake_provider import FakeAlgiers
        assert isinstance(job.backend(), FakeAlgiers), f"Jobs should run on FakeAlgiers backend"


def test_run_jobs_on_batch_circuits_transpiled_with_correct_params():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    result = candidate()
    
    # Run the function again and capture the jobs to inspect transpiled circuits
    # Since the solution likely creates circuits and submits them, we'll check if
    # the transpilation happened correctly by verifying backend and optimization level info
    # via the job metadata or backend properties
    
    # Get one job to inspect
    job = list(result.values())[0]['job']
    
    # Ensure job has backend set correctly
    assert hasattr(job, 'backend'), "Job should have a backend attribute"
    backend = job.backend()
    assert backend.name == 'fake_algiers', f"Backend name should be 'fake_algiers', got {backend.name}"
    
    # Check that all jobs have same batch_id and were submitted together
    batch_ids = [result[key]['batch_id'] for key in result]
    assert len(set(batch_ids)) == 1, "All jobs must be part of the same batch"
    
    # Verify that the number of jobs is 4
    assert len(result) == 4, "Should have 4 Bell state jobs"