from qiskit import QuantumCircuit
from qiskit.circuit.library import C3SXGate
def create_c3sx_circuit() -> QuantumCircuit:
    """ Create a QuantumCircuit with a C3SXGate applied to the first four qubits.
    """

    qc = QuantumCircuit(4)
    c3sx_gate = C3SXGate()
    qc.append(c3sx_gate, [0, 1, 2, 3])
    return qc
