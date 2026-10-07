from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
import numpy as np
def get_unitary() -> np.ndarray:
    """ Get unitary matrix for a phi plus bell circuit and return it.
    """

    circ = QuantumCircuit(2)
    circ.h(0)
    circ.cx(0, 1)
    return Operator.from_circuit(circ).to_matrix()