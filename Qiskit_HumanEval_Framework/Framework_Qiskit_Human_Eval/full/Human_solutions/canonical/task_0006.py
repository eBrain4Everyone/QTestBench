from qiskit import QuantumCircuit


def create_state_prep(num_qubits):
    """ Return a QuantumCircuit that prepares the state |1> on an n-qubit register.
    """

    qc = QuantumCircuit(num_qubits)
    qc.prepare_state(1)
    return qc
