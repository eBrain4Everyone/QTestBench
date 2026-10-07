def check(candidate):
    result = candidate()
    assert type(result) == Figure
    assert len(result.axes) == 2
