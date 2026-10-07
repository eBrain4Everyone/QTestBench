def check(candidate):
    def is_multiple_of_identity(matrix):
        if matrix.shape[0] != matrix.shape[1]:
            return False  # Not a square matrix
        identity_matrix = np.eye(matrix.shape[0])
        scalar = matrix[0,0]
        return np.allclose(matrix, scalar*identity_matrix)
    test_pauli = SparsePauliOp(["XI"])
    can_anticommutators = candidate(test_pauli)
    assert len(can_anticommutators) == 10, "The number of anticommutators is not 10"
    for _,item in enumerate(can_anticommutators):
        assert is_multiple_of_identity(anti_commutator(item, test_pauli).to_matrix()), "The operator doesn't anticommute with the given pauli operator"
