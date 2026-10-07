from qiskit.quantum_info import Statevector
from math import sqrt
def create_bell_statevector() -> Statevector:
    """ Return a phi+ Bell statevector.
    """

    return (Statevector.from_label("00") + Statevector.from_label("11")) / sqrt(2)
