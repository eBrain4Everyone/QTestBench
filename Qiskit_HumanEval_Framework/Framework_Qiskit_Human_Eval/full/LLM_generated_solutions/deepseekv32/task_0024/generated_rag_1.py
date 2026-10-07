# LLM-generated solution — task_0024
# Generated: 2026-06-23T18:08:40.701135
# Model: deepseekv32
# Variant: generated_rag_1

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
    result = job.result()[0]
    
    counts = result.data.meas.get_counts()
    
    measured_bits = list(counts.keys())[0]
    return all(bit == '0' for bit in measured_bits)
