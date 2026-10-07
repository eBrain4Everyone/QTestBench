# LLM-generated solution — task_0024
# Generated: 2026-06-23T18:08:30.568240
# Model: deepseekv32
# Variant: generated_non_rag_3

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from numpy import isclose
def dj_algorithm(oracle: QuantumCircuit) -> bool:
    """ Given a Deutsch-Jozsa oracle in which the final qubit is the "output" qubit, return True if the oracle is constant or False otherwise.
    """
    n = oracle.num_qubits - 1
    qc = QuantumCircuit(n + 1, n)
    for qubit in range(n):
        qc.h(qubit)
    qc.x(n)
    qc.h(n)
    qc.compose(oracle, inplace=True)
    for qubit in range(n):
        qc.h(qubit)
    qc.measure(range(n), range(n))
    sampler = StatevectorSampler()
    job = sampler.run([qc], shots=1)
    result = job.result()
    sample = result[0].data.meas.get_bitstring_counts()
    measured_bitstring = list(sample.keys())[0]
    if int(measured_bitstring, 2) == 0:
        return True
    else:
        return False
