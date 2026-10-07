from qiskit import QuantumCircuit
from numpy import pi
def chsh_circuit(alice: int, bob: int)->QuantumCircuit:
    """ Design a CHSH circuit that takes bits of Alice and Bob as input and return the Quantum Circuit after measuring.
    """

    qc = QuantumCircuit(2,  2)
    qc.h(0)
    qc.cx(0, 1)
    qc.barrier()
    if alice == 0:
        qc.ry(0, 0)
    else:
        qc.ry(-pi / 2, 0)
    qc.measure(0, 0)
    if bob == 0:
        qc.ry(-pi / 4, 1)
    else:
        qc.ry(pi / 4, 1)
    qc.measure(1, 1)
    return qc
