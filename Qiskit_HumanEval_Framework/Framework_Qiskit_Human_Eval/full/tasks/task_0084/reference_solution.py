from qiskit import QuantumCircuit
from qiskit.circuit.library import U3Gate
def controlled_custom_unitary_circuit():
    """ Create a 2-qubit quantum circuit where you define a custom 1-qubit unitary gate (e.g., U3) and apply it as a controlled gate with qubit 0 as control and qubit 1 as target. Return the final circuit.
    """

    qc = QuantumCircuit(2)
    custom_gate = U3Gate(0.3, 0.2, 0.1).control()
    qc.append(custom_gate, [0, 1])
    return qc
