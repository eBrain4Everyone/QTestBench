def check(candidate):
    result = candidate()
    assert isinstance(result, dict)
    assert result.keys() == {"00", "11"}
    assert 0.4 < (result["00"] / sum(result.values())) < 0.6
