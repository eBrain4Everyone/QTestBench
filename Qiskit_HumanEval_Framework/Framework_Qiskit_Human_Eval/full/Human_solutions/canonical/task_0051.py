from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.circuit import Instruction
def quantum_teleportation_circuit(data: [Instruction])->QuantumCircuit:
    """ Write a function to build a quantum teleportation circuit that takes a list of instructions as an argument to transfer the data from the sender to the receiver while taking advantage of dynamic circuits.
    """

    sender = QuantumRegister(1, "sender")
    receiver = QuantumRegister(1, "receiver")
    ancillary = QuantumRegister(1, "ancillary")
    c_sender = ClassicalRegister(1, "c_sender")
    c_receiver = ClassicalRegister(1, "c_receiver")
    c_ancillary = ClassicalRegister(1, "c_ancillary")
    circuit = QuantumCircuit(sender, ancillary, receiver, c_sender, c_ancillary, c_receiver)
    for gate in data:
        circuit.append(gate, [0])
    circuit.barrier()
    circuit.h(ancillary)
    circuit.cx(ancillary, receiver)
    circuit.barrier()
    circuit.cx(sender, ancillary)
    circuit.h(sender)
    circuit.measure(sender, c_sender)
    circuit.measure(ancillary, c_ancillary)
    circuit.barrier()
    with circuit.if_test((c_ancillary, 1)):
        circuit.x(receiver)
    with circuit.if_test((c_sender, 1)):
        circuit.z(receiver)
    circuit.barrier()
    circuit.measure(receiver, c_receiver)
    return circuit
