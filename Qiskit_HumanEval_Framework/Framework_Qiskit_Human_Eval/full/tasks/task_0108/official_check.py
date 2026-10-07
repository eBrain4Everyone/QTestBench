def check(candidate):
    data = np.eye(4)
    choi, adjoint_choi, composed_choi = candidate(data, data)
    assert isinstance(choi, Choi), f'Expected choi to be Choi, but got {type(choi)}'
    assert choi.dim == (2, 2), f'Expected dimensions to be (2, 2), but got {choi.dim}'
    assert isinstance(adjoint_choi, Choi), f'Expected adjoint_choi to be Choi, but got {type(adjoint_choi)}'
    assert isinstance(composed_choi, Choi), f'Expected composed_choi to be Choi, but got {type(composed_choi)}'
    expected_adjoint_data = data.conj().T
    assert np.allclose(adjoint_choi.data, expected_adjoint_data), f'Expected adjoint data to be {expected_adjoint_data}, but got {adjoint_choi.data}'
