def check(candidate):
    result = candidate()
    assert isinstance(result, list)
    for job in result:
        assert hasattr(job, "job_id")
        assert hasattr(job, "creation_date")
        assert job.creation_date.replace(tzinfo=None) >= (datetime.datetime.now() - datetime.timedelta(days=90)).replace(tzinfo=None)
