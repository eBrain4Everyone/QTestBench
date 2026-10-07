from qiskit.circuit import QuantumCircuit, Parameter
def rx_gate(value=None):
    """ Return a 1-qubit QuantumCircuit with a parametrized Rx gate and parameter "theta". If value is not None, return the circuit with value assigned to theta.
    """

    theta = Parameter("theta")
    quantum_circuit = QuantumCircuit(1)
    quantum_circuit.rx(theta, 0)
    if value is not None:
        return quantum_circuit.assign_parameters({theta: value})
    return quantum_circuit
