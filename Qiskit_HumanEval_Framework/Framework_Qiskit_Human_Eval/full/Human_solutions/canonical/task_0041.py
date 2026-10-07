from qiskit.quantum_info.operators import Operator, Pauli
import numpy as np
def compose_op() -> Operator:
    """ Compose XZ with a 3-qubit identity operator using the Operator and the Pauli 'YX' class in Qiskit. Return the operator instance.
    """

    op = Operator(np.eye(2 ** 3))
    YX = Operator(Pauli('YX'))
    composition = op.compose(YX, qargs=[0, 2], front=True)
    return composition
