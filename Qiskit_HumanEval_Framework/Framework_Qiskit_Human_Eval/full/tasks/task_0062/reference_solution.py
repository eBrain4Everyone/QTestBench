from qiskit import QuantumCircuit
def bb84_senders_circuit(state: [int], basis: [int])->QuantumCircuit:
    """ Construct a BB84 protocol circuit for the sender, inputting both the states and the measured bases.
    """

    num_qubits = len(state)
    circuit = QuantumCircuit(num_qubits)
    for i in range(len(basis)):
        if state[i] == 1:
            circuit.x(i)
        if basis[i] == 1:
            circuit.h(i)
    return circuit
