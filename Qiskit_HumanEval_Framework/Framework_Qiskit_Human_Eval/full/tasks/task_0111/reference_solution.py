from qiskit.circuit import QuantumCircuit, Parameter
def circuit():
    """ Return an ansatz to create a quantum dataset of pure states distributed equally across the bloch sphere. Use minimum number of gates in the ansatz.
    """

    qc = QuantumCircuit(1)
    p1 = Parameter("p1")
    p2 = Parameter("p2")
    qc.rx(p1,0)
    qc.ry(p2,0)
    return qc
