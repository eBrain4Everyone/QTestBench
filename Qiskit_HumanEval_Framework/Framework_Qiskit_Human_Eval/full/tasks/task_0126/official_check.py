def check(candidate):
    result = candidate()
    assert isinstance(result, float)
    assert abs(result - 1.0) < 1e-6
