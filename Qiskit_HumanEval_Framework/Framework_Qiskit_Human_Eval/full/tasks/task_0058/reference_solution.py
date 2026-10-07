from qiskit import QuantumCircuit
from numpy import pi
def create_ch_gate()->QuantumCircuit:
    """ Design a CH gate using CX and RY gates.
    """

    circuit = QuantumCircuit(2)
    circuit.ry(pi/4, 1)
    circuit.cx(0,1)
    circuit.ry(-pi/4, 1)
    return circuit
