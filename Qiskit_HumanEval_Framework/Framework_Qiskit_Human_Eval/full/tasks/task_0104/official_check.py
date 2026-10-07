def check(candidate):
    complexity_can = candidate()
    complexity_exp = 197
    assert complexity_can == complexity_exp
