def check(candidate):
    import numpy as np
    from qiskit.quantum_info import Statevector
    def statevector_to_bloch_angles(state_vector):
        alpha = state_vector[0]
        beta = state_vector[1]
        norm = np.sqrt(np.abs(alpha)**2 + np.abs(beta)**2)
        alpha = alpha / norm
        beta = beta / norm
        theta = 2 * np.arccos(np.abs(alpha))
        phi = np.angle(beta) - np.angle(alpha)
        phi = (phi + 2 * np.pi) % (2 * np.pi)
        return theta, phi
    error = 0.000001
    for i in range(1000):
        qc = candidate()
        num_params = qc.num_parameters
        qc.assign_parameters(np.random.randn(num_params), inplace=True)
        sv = Statevector(qc)
        theta, phi = statevector_to_bloch_angles(sv)
        assert np.pi/2 - error <= theta <= np.pi/2 + error
