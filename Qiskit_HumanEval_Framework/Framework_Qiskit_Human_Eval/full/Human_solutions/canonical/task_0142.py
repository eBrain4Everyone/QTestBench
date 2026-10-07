from qiskit.quantum_info import random_density_matrix, purity, DensityMatrix
import numpy as np
def purity_dataset():
    """ Return a list of 10 single qubit density matrices whose purity is greater than 0.5.
    """

    purity_dataset_list = []
    while len(purity_dataset_list)<=9:
        rand_density_matrix = random_density_matrix(dims=2)
        if np.abs(purity(rand_density_matrix))>=0.5:
            purity_dataset_list.append(rand_density_matrix)
    return purity_dataset_list
