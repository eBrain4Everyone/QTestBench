def check(candidate):
    result = candidate()
    assert isinstance(result, dict)
    assert (result["00"] + result["11"]) != sum(result.values())
