from qiskit import QuantumCircuit
import qiskit.qasm3
def convert_quantum_circuit_to_qasm_string(circuit: QuantumCircuit) -> str:
    """ Given a Quantum Circuit as the argument, convert it into qasm3 string and return it.
    """

    qasm_str = qiskit.qasm3.dumps(circuit)
    return qasm_str
