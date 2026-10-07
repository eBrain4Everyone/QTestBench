def check(candidate):
    result = candidate()
    assert isinstance(result, list)
    assert len(result) > 0
    assert set(result) == {"00", "11"}
