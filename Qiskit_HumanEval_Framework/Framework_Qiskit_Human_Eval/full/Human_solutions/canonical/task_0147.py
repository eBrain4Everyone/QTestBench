from qiskit import QuantumCircuit
from qiskit.circuit.library import YGate
def mcy(qc: QuantumCircuit) -> QuantumCircuit:
    """ Add a multi-controlled-Y operation to qubit 4, controlled by qubits 0-3.
    """

    mcy_gate = YGate().control(num_ctrl_qubits=4)
    qc.append(mcy_gate, range(5))
    return qc
