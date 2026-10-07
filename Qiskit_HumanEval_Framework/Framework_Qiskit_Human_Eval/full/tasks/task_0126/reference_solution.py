from qiskit.circuit.library import HGate
from qiskit.quantum_info import Operator, process_fidelity
import numpy as np
def calculate_phase_difference_fidelity():
    """ Create two quantum operators using Hadamard gate that differ only by a global phase. Calculate the process fidelity between these two operators and return the process fidelity value.
    """

    op_a = Operator(HGate())
    op_b = np.exp(1j * 0.5) * Operator(HGate())
    
    fidelity = process_fidelity(op_a, op_b)
    
    return fidelity
