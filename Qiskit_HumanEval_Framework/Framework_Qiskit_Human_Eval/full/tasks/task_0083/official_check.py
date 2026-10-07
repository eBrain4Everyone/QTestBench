def check(candidate):
    import numpy as np
    DensityMatrix, concurrence = candidate()
    assert round(concurrence,1) == 1
    expected_rho = np.array([[0.5, 0, 0, 0.5], [0, 0, 0, 0], [0, 0, 0, 0], [0.5, 0, 0, 0.5]])
    np.testing.assert_array_almost_equal(DensityMatrix, expected_rho, decimal=5, err_msg='Density matrix does not match the expected Bell state density matrix')
