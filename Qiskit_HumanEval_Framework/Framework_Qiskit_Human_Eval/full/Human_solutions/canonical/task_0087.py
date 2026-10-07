from qiskit import QuantumCircuit
def quantum_circuit_with_delay():
    """ Create a one-qubit quantum circuit, apply hadamard gate, then add a delay of 100 and then again apply hadamard gate and return the circuit.
    """

    qc = QuantumCircuit(1)
    qc.h(0)
    delay_duration = 100
    qc.delay(delay_duration, 0, unit="dt")
    qc.h(0)
    return qc
