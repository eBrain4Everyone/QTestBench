from qiskit.circuit.library import Diagonal
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
def create_diagonal_circuit(diag: list) -> QuantumCircuit:
    """ Create a QuantumCircuit with a Diagonal gate applied to the qubits.
    The diagonal elements are provided in the list 'diag'.
    """

    diagonal_gate = Diagonal(diag)
    qc = QuantumCircuit(diagonal_gate.num_qubits)
    qc.append(diagonal_gate.to_instruction(), range(diagonal_gate.num_qubits))
    return qc
