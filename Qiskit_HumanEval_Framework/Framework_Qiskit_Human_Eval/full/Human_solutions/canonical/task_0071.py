from qiskit import QuantumCircuit
def create_quantum_circuit_based_h0_csx01_h1():
    """ Build a Quantum Circuit composed by the gates H in Quantum register 0, Controlled-√X gate in quantum register 0 1, and H gate in quantum register 1.
    """

    qc = QuantumCircuit(2)
    qc.h(0)
    qc.csx(0,1)
    qc.h(1)
    return qc
