from qiskit import QuantumCircuit
def create_state_prep():
    """ Return a QuantumCircuit that prepares the binary state 1.
    """

    qc = QuantumCircuit(2)
    qc.prepare_state("01")
    return qc
