def check(candidate):
    result = candidate()
    assert result == {"00": 521, "11": 503}
