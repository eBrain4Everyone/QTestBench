# LLM-generated solution — task_0024
# Generated: 2026-06-23T18:24:58.575063
# Model: gemini3pro
# Variant: generated_non_rag_3

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.primitives import StatevectorSampler
from numpy import isclose

def dj_algorithm(oracle: QuantumCircuit) -> bool:
    """ Given a Deutsch-Jozsa oracle in which the final qubit is the "output" qubit, return True if the oracle is constant or False otherwise.
    """
    N = oracle.num_qubits
    n = N - 1
    if n <= 0:
        return True
        
    qr = QuantumRegister(N, 'q')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qr, cr)
    
    qc.x(n)
    qc.h(range(N))
    
    qc.compose(oracle, qubits=range(N), inplace=True)
    
    qc.h(range(n))
    qc.measure(range(n), range(n))
    
    sampler = StatevectorSampler()
    job = sampler.run([qc], shots=1)
    result = job.result()[0]
    
    counts = result.data.c.get_counts()
    
    all_zeros = "0" * n
    return all_zeros in counts
