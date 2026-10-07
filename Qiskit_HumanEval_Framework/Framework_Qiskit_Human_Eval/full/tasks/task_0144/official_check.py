def check(candidate):
    can_mat_list = candidate()
    assert len(can_mat_list) == 10, "The list doesn't contain 10 elements"
    for _, item in enumerate(can_mat_list):
        assert isinstance(item, DensityMatrix)
        assert concurrence(item) == 0, "The concurrence of the density matrix is not 0"
