from qiskit import QuantumCircuit
from qiskit.quantum_info import DensityMatrix, concurrence
def calculate_bell_state_properties():
    """ Construct a Phi plus Bell state quantum circuit, compute its Density Matrix and Concurrence, and return these results in a tuple in the same order.
    """

    qc = QuantumCircuit(2, name='Bell')
    qc.h(0)
    qc.cx(0, 1)
    rho = DensityMatrix.from_instruction(qc)
    concur = concurrence(rho)
    return rho, concur
