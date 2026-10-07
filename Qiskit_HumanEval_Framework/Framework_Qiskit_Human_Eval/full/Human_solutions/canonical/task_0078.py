from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT


def qft_no_swaps(num_qubits: int) -> QuantumCircuit:
    """ Return an inverse quantum Fourier transform circuit without the swap gates.
    """

    qft = QFT(num_qubits=num_qubits, do_swaps=False, inverse=True)
    return qft
