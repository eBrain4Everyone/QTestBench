def check(candidate):
    from qiskit.quantum_info import DensityMatrix
    tol = 0.1
    can_list = candidate(tol)
    assert len(can_list) == 10, "Length of list is not 10"
    for _, item in enumerate(can_list):
        assert isinstance(item, DensityMatrix), "The list doesn't contain density matrices"
        assert entanglement_of_formation(item) >= tol , " The entanglement of formation is not within tolerance"
