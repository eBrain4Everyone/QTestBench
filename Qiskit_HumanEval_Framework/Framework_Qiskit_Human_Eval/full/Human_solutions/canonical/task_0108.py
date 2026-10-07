from qiskit.quantum_info import Choi
import numpy as np
def initialize_adjoint_and_compose(data1: np.ndarray, data2: np.ndarray) -> (Choi, Choi, Choi):
    """ Initialize Choi matrices for the given data1 and data2 as inputs. Compute data1 adjoint, and then return the data1 Choi matrix, its adjoint and the composed choi matrices in order.
    """

    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
