from qiskit.circuit.random import random_circuit
from qiskit import QuantumCircuit
def random_circuit_depth():
    """ Using qiskit's random_circuit function, generate a circuit with 4 qubits and a depth of 3 that measures all qubits at the end. Use the seed value 17 and return the generated circuit.
    """

    circuit = random_circuit(4, 3, measure=True, seed = 17)
    return circuit
