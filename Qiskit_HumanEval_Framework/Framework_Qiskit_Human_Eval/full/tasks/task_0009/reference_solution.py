from qiskit.circuit.library import efficient_su2
def create_efficientSU2():
    """ Generate an EfficientSU2 circuit with 3 qubits, 1 reps and make insert_barriers true.
    """

    circuit = efficient_su2(num_qubits=3, reps=1, insert_barriers=True)
    return circuit
