from qiskit import QuantumRegister, QuantumCircuit, ClassicalRegister
def create_quantum_circuit_with_one_qubit_and_measure():
    """ Build a Quantum Circuit by first creating one Quantum Register and one Classical Register and then perform measurement on it.
    """

    q = QuantumRegister(1, 'q')
    c = ClassicalRegister(1, 'c')
    qc = QuantumCircuit(q, c)
    qc.measure(q, c)
    return qc
