# LLM-generated solution — task_0024
# Generated: 2026-06-23T18:23:23.694941
# Model: gemini3pro
# Variant: generated_non_rag_1

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from numpy import isclose

def dj_algorithm(oracle: QuantumCircuit) -> bool:
    n = oracle.num_qubits - 1
    if n == 0:
        return True
        
    qc = QuantumCircuit(n + 1, n)
    
    qc.x(n)
    for i in range(n + 1):
        qc.h(i)
        
    qc.compose(oracle, inplace=True)
    
    for i in range(n):
        qc.h(i)
        qc.measure(i, i)
        
    sampler = StatevectorSampler()
    job = sampler.run([qc], shots=1)
    result = job.result()[0]
    
    counts = getattr(result.data, qc.cregs[0].name).get_counts()
    measured_str = list(counts.keys())[0]
    
    return all(bit == '0' for bit in measured_str)
