def check(candidate):
    from numpy import isclose
    jobs = candidate()
    reference_data = {
        'phi_plus': {'00': 0.10, '11': 0.10},
        'phi_minus': {'00': 0.10, '11': 0.10},
        'psi_plus': {'01': 0.10, '10': 0.10},
        'psi_minus': {'01': 0.1, '10': 0.10}
    }
    assert isinstance(jobs, dict)
    assert set(jobs.keys()) == set(reference_data.keys())
    for state, job in jobs.items():
        assert isinstance(job, PrimitiveJob)
        assert job.job_id() is not None
        counts = job.result()[0].data.meas.get_counts()
        shots = 4096
        normalized_counts = {k: v/shots for k, v in counts.items()}
        for key, value in reference_data[state].items():
            assert isclose(normalized_counts[key], value, atol=1e-01)
