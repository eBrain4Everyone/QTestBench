from qiskit import QuantumCircuit
from numpy import arccos, sqrt
def w_state()->QuantumCircuit:
    """ Generate a Quantum Circuit for a W state and measure it.
    """

    circuit = QuantumCircuit(3)
    circuit.ry(2*arccos(1/sqrt(3)), 0)
    circuit.ch(0,1)
    circuit.cx(1,2)
    circuit.cx(0,1)
    circuit.x(0)
    circuit.measure_all()
    return circuit
