# LLM-generated solution — task_0024
# Generated: 2026-06-23T18:51:34.805305
# Model: qwen3
# Variant: generated_rag_1

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from numpy import isclose
import numpy as np

def dj_algorithm(oracle: QuantumCircuit) -> bool:
    """ Given a Deutsch-Jozsa oracle in which the final qubit is the "output" qubit, return True if the oracle is constant or False otherwise.
    """
    n = oracle.num_qubits - 1  # Number of input qubits
    qc = QuantumCircuit(n + 1, n)
    
    # Initialize |0...0> |1> state
    qc.x(n)  # Set the output qubit to |1>
    
    # Apply Hadamard gates to all qubits
    for i in range(n + 1):
        qc.h(i)
    
    # Apply the oracle
    qc.compose(oracle, inplace=True)
    
    # Apply Hadamard gates to the input qubits only
    for i in range(n):
        qc.h(i)
    
    # Measure only the input qubits
    qc.measure(list(range(n)), list(range(n)))
    
    # Use StatevectorSampler to get the final state before measurement
    sampler = StatevectorSampler()
    result = sampler.run(qc, shots=1).result()
    state = result.quasi_dists[0  # Get the first (and only) sample's state
    # For a constant function, the measurement should yield |0...0> with probability 1
    # For a balanced function, it should not
    zero_state_prob = state.get(0, 0)
    
    return isclose(zero_state_prob, 1.0, atol=1e-10)
