def check(candidate):
    s = "1111"
    result = candidate(s)
    assert (type(result[0]) == list)
    assert (len(result[0]) == result[1][0].data.meas.num_shots)
    assert (type(result[1]) == PrimitiveResult)
