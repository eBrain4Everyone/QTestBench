from qiskit_aer.noise import NoiseModel, ReadoutError
def noise_model_with_readouterror():
    """ Construct a noise model with specific readout error properties for different qubits. For qubit 0, a readout of 1 has a 20% probability 
    of being erroneously read as 0, and a readout of 0 has a 30% probability of being erroneously read as 1. For all other qubits, a readout of 1 has a 3% 
    probability of being erroneously read as 0, and a readout of 0 has a 2% probability of being erroneously read as 1.
    """

    noise_model = NoiseModel()
    p0given1_other = 0.03
    p1given0_other = 0.02
    readout_error_other = ReadoutError(
        [
            [1 - p1given0_other, p1given0_other],
            [p0given1_other, 1 - p0given1_other],
        ]
    )
    noise_model.add_all_qubit_readout_error(readout_error_other)

    p0given1_q0 = 0.2
    p1given0_q0 = 0.3
    readout_error_q0 = ReadoutError(
        [
            [1 - p1given0_q0, p1given0_q0],
            [p0given1_q0, 1 - p0given1_q0],
        ]
    )
    noise_model.add_readout_error(readout_error_q0, [0])

    return noise_model
