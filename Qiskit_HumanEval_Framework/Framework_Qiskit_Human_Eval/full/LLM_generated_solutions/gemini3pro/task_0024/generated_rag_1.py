# LLM-generated solution — task_0024
# Generated: 2026-06-23T18:25:50.819945
# Model: gemini3pro
# Variant: generated_rag_1

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.primitives import StatevectorSampler
from numpy import isclose

def dj_algorithm(oracle: QuantumCircuit) -> bool:
    """ Given a Deutsch-Jozsa oracle in which the final qubit is the "output" qubit, return True if the oracle is constant or False otherwise.
    """
    n_qubits = oracle.num_qubits
    n = n_qubits - 1
    
    qr = QuantumRegister(n_qubits, 'q')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qr, cr)
    
    # Initialize output qubit to |->
    qc.x(n)
    for i in range(n_qubits):
        qc.h(i)
        
    # Apply oracle
    qc.compose(oracle, qubits=range(n_qubits), inplace=True)
    
    # Apply H to input qubits and measure
    for i in range(n):
        qc.h(i)
        qc.measure(i, i)
        
    # Execute the circuit
    sampler = StatevectorSampler()
    job = sampler.run([qc], shots=1024)
    result = job.result()[0]
    
    # Process results
    counts = result.data.c.get_counts()
    zero_str = '0' * n
    
    total_shots = sum(counts.values())
    zero_count = counts.get(zero_str, 0)
    
    # Return True if constant (all zeros measured), False if balanced
    return bool(isclose(zero_count / total_shots, 1.0))
