# LLM-generated solution — task_0024
# Generated: 2026-06-23T18:24:20.904141
# Model: gemini3pro
# Variant: generated_non_rag_2

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from numpy import isclose

def dj_algorithm(oracle: QuantumCircuit) -> bool:
    """ Given a Deutsch-Jozsa oracle in which the final qubit is the "output" qubit, return True if the oracle is constant or False otherwise.
    """
    n_qubits = oracle.num_qubits
    n = n_qubits - 1
    
    if n == 0:
        return True
        
    qc = QuantumCircuit(n_qubits, n)
    
    qc.x(n)
    
    for i in range(n_qubits):
        qc.h(i)
        
    qc.compose(oracle, inplace=True)
    
    for i in range(n):
        qc.h(i)
        
    qc.measure(range(n), range(n))
    
    sampler = StatevectorSampler()
    shots = 1024
    job = sampler.run([qc], shots=shots)
    result = job.result()[0]
    
    cr_name = qc.cregs[0].name
    counts = getattr(result.data, cr_name).get_counts()
    
    prob = counts.get('0' * n, 0) / shots
    return bool(isclose(prob, 1.0))
