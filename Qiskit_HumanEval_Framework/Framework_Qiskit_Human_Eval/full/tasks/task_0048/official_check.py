def check(candidate):
    result = candidate(10)
    assert isinstance(result, list)
    assert len(result) == 10
    for i in range(10):
        assert result[i] >= 0 and result[i] < 256
