from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
def create_uniform_superposition(n: int) -> Statevector:
    """ Initialize a uniform superposition on n qubits and return statevector.
    """

    qc = QuantumCircuit(n)
    qc.h(range(n))
    return Statevector(qc)
