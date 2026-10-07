def check(candidate):
    result = candidate()
    assert result.depth() == 1
    assert result.width() == 2
    assert dict(result.count_ops()) == {'measure': 1}
