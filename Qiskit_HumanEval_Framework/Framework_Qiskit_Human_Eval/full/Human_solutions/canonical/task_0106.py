from qiskit import QuantumCircuit
from qiskit.quantum_info import CNOTDihedral
def compose_cnot_dihedral() -> CNOTDihedral:
    """ Create two Quantum Circuits of 2 qubits. First quantum circuit should have a cx gate on qubits 0 and 1 and a T gate on qubit 0. The second one is the same but with an additional X gate on qubit 1. Convert the two quantum circuits into CNOTDihedral elements and return the composed circuit.
    """

    circ1 = QuantumCircuit(2)
    # Apply gates
    circ1.cx(0, 1)
    circ1.t(0)
    elem1 = CNOTDihedral(circ1)
    circ2 = circ1.copy()
    circ2.x(1)
    elem2 = CNOTDihedral(circ2)
    composed_elem = elem1.compose(elem2)
    return composed_elem
