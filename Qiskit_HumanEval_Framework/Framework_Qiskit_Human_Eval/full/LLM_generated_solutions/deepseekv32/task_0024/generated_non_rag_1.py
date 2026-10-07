# LLM-generated solution — task_0024
# Generated: 2026-06-23T18:07:57.101936
# Model: deepseekv32
# Variant: generated_non_rag_1

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from numpy import isclose

def dj_algorithm(oracle: QuantumCircuit) -> bool:
    """ Given a Deutsch-Jozsa oracle in which the final qubit is the "output" qubit, return True if the oracle is constant or False otherwise.
    """
    n = oracle.num_qubits - 1
    qc = QuantumCircuit(n + 1, n)
    for i in range(n):
        qc.h(i)
    qc.x(n)
    qc.h(n)
    qc.compose(oracle, range(n + 1), inplace=True)
    for i in range(n):
        qc.h(i)
    qc.measure(range(n), range(n))
    
    sampler = StatevectorSampler()
    job = sampler.run([qc], shots=1)
    result = job.result()
    sampled = result[0].data.c.get_counts()
    measured = next(iter(sampled.keys()))
    all_zeros = '0' * n
    return measured == all_zeros
