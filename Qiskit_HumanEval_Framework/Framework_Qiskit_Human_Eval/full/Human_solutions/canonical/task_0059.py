from qiskit import QuantumCircuit
def create_cz_gate()->QuantumCircuit:
    """ Design a CZ gate using only H and CNOT gates and return the quantum circuit.
    """

    circuit = QuantumCircuit(2)
    circuit.h(1)
    circuit.cx(0,1)
    circuit.h(1)
    return circuit
