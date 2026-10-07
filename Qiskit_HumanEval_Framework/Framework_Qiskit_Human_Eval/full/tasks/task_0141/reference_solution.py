from qiskit.quantum_info import anti_commutator, SparsePauliOp
from qiskit.quantum_info import random_pauli
import numpy as np
def anticommutators(pauli: SparsePauliOp):
    """ Return a list of ten Pauli operators whose anticommutator with the given Pauli is a multiple of the identity.
    """

    def is_multiple_of_identity(matrix):
        identity_matrix = np.eye(matrix.shape[0])
        scalar = matrix[0,0]
        return np.allclose(matrix, scalar*identity_matrix)
    num_qubits = pauli.num_qubits
    anticommutator_list = []
    while len(anticommutator_list) <= 9:
        random_pauli_value = SparsePauliOp(random_pauli(num_qubits))
        anti_commutator_value = anti_commutator(pauli, random_pauli_value)
        if is_multiple_of_identity(anti_commutator_value.to_matrix()):
            anticommutator_list.append(random_pauli_value)
    return anticommutator_list
