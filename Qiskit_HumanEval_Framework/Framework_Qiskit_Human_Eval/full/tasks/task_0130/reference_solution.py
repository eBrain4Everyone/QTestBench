from qiskit.circuit import QuantumCircuit
def inv_circuit(n):
    """ Create a quantum circuit with 'n' qubits. Apply Hadamard gates to the second and third qubits.
    Then apply CNOT gates between the second and fourth qubits, and between the third and fifth qubits.
    Finally give the inverse of the quantum circuit.
    """

    qc = QuantumCircuit(n)
    for i in range(2):
        qc.h(i+1)

    for i in range(2):
        qc.cx(i+1, i+2+1)
    
    return qc.inverse()
