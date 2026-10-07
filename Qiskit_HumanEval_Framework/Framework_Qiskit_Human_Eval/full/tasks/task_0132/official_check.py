def check(candidate):
    result = candidate()
    assert isinstance(result, list)
    assert len(result) == 2
    for counts in result:
        assert isinstance(counts, dict)
        assert counts == {"110": 423, "100": 474, "000": 58, "010": 52, "101": 8, "111": 8, "011": 1}
