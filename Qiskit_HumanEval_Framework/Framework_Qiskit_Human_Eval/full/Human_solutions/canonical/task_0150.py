from qiskit import QuantumCircuit
from numpy import pi
def for_loop_circuit(qc: QuantumCircuit, n: int) -> QuantumCircuit:
    """ Add a sub-circuit to the quantum circuit `qc` that applies a series of operations for `n` iterations using the `for_loop`.

    In each iteration `i`, perform the following:
    1. Apply a `RY` rotation on qubit 0 with an angle of `pi/n * i`.
    2. Apply a Hadamard gate to qubit 0 and a CNOT gate between qubits 0 and 1 to create a phi plus Bell state.
    3. Measure qubit 0 and store the result in the corresponding classical register.
    4. Break the loop if the classical register for qubit 0 measures the value 1.

    Use the `for_loop` control flow structure to implement the loop and include conditional breaking based on the measurement.
    """

    with qc.for_loop(range(n)) as i:
        qc.ry(pi/n*i, 0)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure(0, 0)
        with qc.if_test((qc.clbits[0], 1)):
            qc.break_loop()
    return qc
