from qiskit.quantum_info import entropy, random_density_matrix, DensityMatrix
def pure_states(ε):
    """ Return a list of ten density matrices which are pure up to a tolerance of ε.
    """

    entropy_list = []
    while len(entropy_list) <= 9:
        density_matrix = random_density_matrix(dims = 2)
        if entropy(density_matrix) < ε:
            entropy_list.append(density_matrix)
    return entropy_list
