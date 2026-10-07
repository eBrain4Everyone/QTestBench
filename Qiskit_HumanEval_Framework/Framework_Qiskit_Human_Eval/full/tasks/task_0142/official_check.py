def check(candidate):
    can_list = candidate()
    assert len(can_list) == 10, "Number of density matrices is not 10"
    for _, item in enumerate(can_list):
        assert isinstance(item, DensityMatrix)
        assert np.abs(purity(item))>=0.5, "Purity of the density matrices is less than 0.5"
