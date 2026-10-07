from qiskit.quantum_info import random_density_matrix, entanglement_of_formation
def entanglement_dataset(ε):
    """ Return a dataset of density matrices whose 2-qubit entanglement of formation is greater than or equal to the given tolerance.
    """

    entanglement_data = []
    while len(entanglement_data) <= 9:
        density_matrix = random_density_matrix(dims = 4)
        if entanglement_of_formation(density_matrix)>=ε:
            entanglement_data.append(density_matrix)
    return entanglement_data
