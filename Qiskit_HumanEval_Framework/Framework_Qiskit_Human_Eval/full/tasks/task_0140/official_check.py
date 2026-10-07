def check(candidate):
    tol = 1
    can_list = candidate(tol)
    assert len(can_list) == 10, " The length of the list is not 10"
    for _, item in enumerate(can_list):
        assert shannon_entropy(item)>= tol, "Shannon entropy not greater than given value"
        assert len(item) == 16, "The length of the probability vector is not 16"
