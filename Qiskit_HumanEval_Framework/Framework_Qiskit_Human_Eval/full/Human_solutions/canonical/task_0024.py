from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from numpy import isclose
def dj_algorithm(oracle: QuantumCircuit) -> bool:
    """ Given a Deutsch-Jozsa oracle in which the final qubit is the "output" qubit, return True if the oracle is constant or False otherwise.
    """

    n = oracle.num_qubits
    qc = QuantumCircuit(n, n - 1)
    qc.x(n - 1)
    qc.h(range(n))
    qc.compose(oracle, inplace=True)
    qc.h(range(n))
    qc.measure(range(n - 1), range(n - 1))
    counts = StatevectorSampler().run([qc]).result()[0].data.c.get_counts()

    all_zeros = '0' * (n - 1)
    return isclose(counts.get(all_zeros, 0), 1024)
