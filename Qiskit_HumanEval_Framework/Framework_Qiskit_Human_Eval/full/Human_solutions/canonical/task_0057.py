from qiskit import QuantumCircuit
def create_swap_gate()->QuantumCircuit:
    """ Design a SWAP gate using only CX gates.
    """

    circuit = QuantumCircuit(2)
    circuit.cx(0,1)
    circuit.cx(1,0)
    circuit.cx(0,1)
    return circuit
