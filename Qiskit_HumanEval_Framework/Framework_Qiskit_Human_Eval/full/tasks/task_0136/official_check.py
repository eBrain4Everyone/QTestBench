def check(candidate):
    tol = 0.01
    list_can = candidate(tol)
    assert len(list_can) == 10," Length of the list is not 10"
    for _, item in enumerate(list_can):
        assert isinstance(item, DensityMatrix), "The list doesn't contain density matrices"
        assert entropy(item) < tol, "Entropy of density matrix is not within tolerance"
