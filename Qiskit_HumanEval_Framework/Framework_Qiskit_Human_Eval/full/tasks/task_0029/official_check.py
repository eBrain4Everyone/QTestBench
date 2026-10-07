def check(candidate):
    result = candidate()
    assert type(result) == Figure
