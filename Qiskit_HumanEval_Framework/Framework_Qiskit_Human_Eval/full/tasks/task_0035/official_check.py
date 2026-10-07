def check(candidate):
    from numpy import isclose
    job = candidate()
    assert isinstance(job, PrimitiveJob)
    assert job.job_id() is not None
    result = job.result()
    assert isclose(result[0].data.evs.item(), 0.33, atol=0.06)
