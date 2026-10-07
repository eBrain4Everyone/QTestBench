from qiskit.quantum_info.random import random_clifford
def get_random_clifford(n_qubits):
    """ Generate a random clifford circuit using the input n_qubit as number of qubits.
    """

    return random_clifford(num_qubits=n_qubits)
