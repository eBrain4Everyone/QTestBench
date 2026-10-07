from qiskit import QuantumCircuit
def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    """ Build a Quantum Circuit composed by the gates H in Quantum register 0, Controlled-S gate in quantum register 0 1, H gate in quantum register 1 and Controlled-S dagger gate in quantum register 1 0.
    """

    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cs(0,1)
    qc.h(1)
    qc.csdg(1,0)
    return qc
