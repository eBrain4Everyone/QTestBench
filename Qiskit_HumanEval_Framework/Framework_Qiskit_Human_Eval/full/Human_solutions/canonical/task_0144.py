from qiskit.quantum_info import random_density_matrix, concurrence, DensityMatrix
def concurrence_dataset():
    """ Return a list of 10 density matrices whose concurrence is 0.
    """

    concurrence_dataset_list = []
    while len(concurrence_dataset_list) <= 9:
        rand_mat = random_density_matrix(dims = 4)
        if concurrence(rand_mat) == 0:
            concurrence_dataset_list.append(rand_mat)
    return concurrence_dataset_list
