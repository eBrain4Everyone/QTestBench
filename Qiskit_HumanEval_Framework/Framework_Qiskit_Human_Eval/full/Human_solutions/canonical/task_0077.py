import math
from qiskit import QuantumCircuit
def circuit_from_probability_dist(probability_dist: dict[int, float]) -> QuantumCircuit:
    """ Given a distribution as a dictionary of the form { measurement: probability }, return a quantum circuit that produces that distribution.
    """

    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    amplitudes = []
    for basis_state in range(2**num_qubits):
        prob = probability_dist.get(basis_state, 0)
        amplitudes.append(math.sqrt(prob))

    qc = QuantumCircuit(num_qubits)
    qc.prepare_state(amplitudes, range(num_qubits))
    return qc
