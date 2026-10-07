# LLM-generated solution — task_0024
# Generated: 2026-06-23T17:58:06.953180
# Model: claudeopus46
# Variant: generated_non_rag_1

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from numpy import isclose


def dj_algorithm(oracle: QuantumCircuit) -> bool:
    """Given a Deutsch-Jozsa oracle in which the final qubit is the "output" qubit,
    return True if the oracle is constant or False otherwise."""
    
    n_qubits = oracle.num_qubits
    n_input = n_qubits - 1  # last qubit is the output qubit
    
    # Create the Deutsch-Jozsa circuit
    dj_circuit = QuantumCircuit(n_qubits, n_input)
    
    # Initialize output qubit to |1_
    dj_circuit.x(n_qubits - 1)
    
    # Apply Hadamard to all qubits
    for i in range(n_qubits):
        dj_circuit.h(i)
    
    # Apply the oracle
    dj_circuit.compose(oracle, inplace=True)
    
    # Apply Hadamard to input qubits
    for i in range(n_input):
        dj_circuit.h(i)
    
    # Measure input qubits
    for i in range(n_input):
        dj_circuit.measure(i, i)
    
    # Run using StatevectorSampler
    sampler = StatevectorSampler()
    job = sampler.run([dj_circuit], shots=1024)
    result = job.result()
    
    pub_result = result[0]
    counts = pub_result.data.c0.get_counts()
    
    # If all input qubits measure 0, the oracle is constant
    all_zeros = '0' * n_input
    
    # Check if the result is all zeros
    if all_zeros in counts and isclose(counts[all_zeros] / 1024, 1.0, atol=0.01):
        return True
    else:
        return False
