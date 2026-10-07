def check(candidate):
    result = candidate()
    assert isinstance(result, list)
    assert result == [{"01": 1024}, {"00": 552, "01": 472}]
