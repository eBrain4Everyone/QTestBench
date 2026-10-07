from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
def conditional_two_qubit_circuit():
    """ Create a quantum circuit with one qubit and two classical bits. The qubit's operation depends on its measurement outcome: if it measures to 1 (|1> state), it flips the qubit's state back to |0> using an X gate. The qubit's initial state is randomized using a Hadamard gate. When building the quantum circuit make sure the classical registers is named 'c'.
    """

    qr = QuantumRegister(1)
    cr = ClassicalRegister(2, 'c')
    qc = QuantumCircuit(qr, cr)

    qc.h(qr[0])
    qc.measure(qr[0], cr[0])
    with qc.if_test((cr[0], 1)):
        qc.x(qr[0])
    qc.measure(qr[0], cr[1])
    return qc
