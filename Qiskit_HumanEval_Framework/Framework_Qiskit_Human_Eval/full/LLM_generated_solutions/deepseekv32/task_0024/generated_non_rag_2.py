# LLM-generated solution — task_0024
# Generated: 2026-06-23T18:08:04.092658
# Model: deepseekv32
# Variant: generated_non_rag_2

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from numpy import isclose

def dj_algorithm(oracle: QuantumCircuit) -> bool:
    """ Given a Deutsch-Jozsa oracle in which the final qubit is the "output" qubit, return True if the oracle is constant or False otherwise.
    """
    n = oracle.num_qubits - 1
    qc = QuantumCircuit(n + 1, n)
    qc.x(n)
    for i in range(n + 1):
        qc.h(i)
    qc.compose(oracle, range(n + 1), inplace=True)
    for i in range(n):
        qc.h(i)
    for i in range(n):
        qc.measure(i, i)
    sampler = StatevectorSampler()
    result = sampler.run([qc], shots=1).result()
    counts = result[0].data.meas.get_counts()
    measured_bits = next(iter(counts.keys()))
    return all(bit == '0' for bit in measured_bits)
