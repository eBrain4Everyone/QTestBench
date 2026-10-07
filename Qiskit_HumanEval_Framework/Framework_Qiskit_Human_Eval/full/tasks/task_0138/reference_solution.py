from qiskit.quantum_info import mutual_information, random_density_matrix
def mutual_information_dataset(ε):
    """ Return a list of density matrices whose mutual information is greater than the given tolerance.
    """

    mutual_information_list = []
    while len(mutual_information_list)<= 9:
        density_matrix = random_density_matrix(dims = 4)
        if mutual_information(density_matrix) >= ε:
            mutual_information_list.append(density_matrix)
    return mutual_information_list
