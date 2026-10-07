from qiskit import QuantumCircuit
def create_custom_controlled()-> QuantumCircuit:
    """ Create a custom 2-qubit gate with an X gate on qubit 0 and an H gate on qubit 1. Then, add two control qubits to this gate. Apply this controlled gate to a 4-qubit circuit, using qubits 0 and 3 as controls and qubits 1 and 2 as targets. Return the final circuit.
    """

    qc1 = QuantumCircuit(2)
    qc1.x(0)
    qc1.h(1)
    custom = qc1.to_gate().control(2)
    qc2 = QuantumCircuit(4)
    qc2.append(custom, [0, 3, 1, 2])
    return qc2
