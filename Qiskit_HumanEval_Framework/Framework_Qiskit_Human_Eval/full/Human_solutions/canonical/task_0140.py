from qiskit.quantum_info import shannon_entropy
import numpy as np
def shannon_entropy_data(ε):
    """ Return a list of ten probability vectors each of length 16 whose shannon entropy is greater than a given value.
    """

    shannon_data = []
    while len(shannon_data) <= 9:
        rand_prob = np.random.dirichlet(np.ones(16))
        if shannon_entropy(rand_prob) >= ε:
            shannon_data.append(rand_prob)
    return shannon_data
