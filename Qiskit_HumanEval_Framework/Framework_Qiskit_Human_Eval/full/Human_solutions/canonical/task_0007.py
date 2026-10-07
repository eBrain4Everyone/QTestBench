from qiskit.circuit import QuantumCircuit, Parameter
def create_parametrized_gate():
    """ Generate a 1 qubit QuantumCircuit with a parametrized Rx gate with parameter "theta".
    """

    theta = Parameter("theta")
    quantum_circuit = QuantumCircuit(1)
    quantum_circuit.rx(theta, 0)
    return quantum_circuit
