from qiskit.circuit.library import QFT
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
def qft_inverse(n: int):
    """ Return the inverse qft circuit for n qubits.
    """

    return QFT(num_qubits=n, approximation_degree=0, inverse=True)
