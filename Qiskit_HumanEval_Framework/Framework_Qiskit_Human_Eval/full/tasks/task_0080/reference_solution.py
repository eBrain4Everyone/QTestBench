from qiskit import QuantumCircuit
from qiskit.circuit import Gate
def count_gates(circuit: QuantumCircuit) -> int:
    """ Return the total number of unitary gates in the circuit.
    """

    count = 0
    for inst in circuit.data:
        if isinstance(inst.operation, Gate):
            count += 1
    return count
