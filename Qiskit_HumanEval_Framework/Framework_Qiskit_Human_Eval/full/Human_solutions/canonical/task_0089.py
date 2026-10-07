from qiskit.circuit.library import HGate
from qiskit import QuantumCircuit, QuantumRegister
def create_controlled_hgate()->QuantumCircuit:
    """ Construct a quantum circuit with a three-qubit controlled-Hadamard gate, using qubit 0 and qubit 1 as the control bits and qubit 2 as the target bit. Return the circuit.
    """

    qr = QuantumRegister(3)
    qc = QuantumCircuit(qr)
    c3h_gate = HGate().control(2)
    qc.append(c3h_gate, qr)
    return qc
