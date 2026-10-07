from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
def send_bits(bitstring: str)->QuantumCircuit:
    """ Provide a quantum circuit that enables the transmission of two classical bits from the sender to the receiver through a single qubit of quantum communication, given that the sender and receiver have access to entangled qubits.
    """

    sender = QuantumRegister(1, "sender")
    receiver = QuantumRegister(1, "receiver")
    measure = ClassicalRegister(2, "measure")
    circuit = QuantumCircuit(sender, receiver, measure)
    # Prepare ebit used for superdense coding
    circuit.h(sender)
    circuit.cx(sender, receiver)
    circuit.barrier()
    # sender's operations
    if bitstring[1] == "1":
        circuit.z(sender)
    if bitstring[0] == "1":
        circuit.x(sender)
    circuit.barrier()
    # receiver's actions
    circuit.cx(sender, receiver)
    circuit.h(sender)
    circuit.measure(sender, measure[0])
    circuit.measure(receiver, measure[1])
    return circuit
