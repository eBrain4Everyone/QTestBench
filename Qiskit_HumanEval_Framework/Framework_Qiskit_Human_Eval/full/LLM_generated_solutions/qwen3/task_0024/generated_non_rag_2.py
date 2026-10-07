# LLM-generated solution — task_0024
# Generated: 2026-06-23T18:51:13.311286
# Model: qwen3
# Variant: generated_non_rag_2

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from numpy import isclose
import numpy as np

def dj_algorithm(oracle: QuantumCircuit) -> bool:
    """ Given a Deutsch-Jozsa oracle in which the final qubit is the "output" qubit, return True if the oracle is constant or False otherwise.
    """
    # Get the number of qubits from the oracle
    n = oracle.num_qubits - 1  # final qubit is output, so n is number of input qubits
    
    # Create the Deutsch-Jozsa circuit
    qc = QuantumCircuit(n + 1, n)
    
    # Initialize |0...0> for input qubits and |1> for output qubit
    qc.x(n)  # Apply X gate to the output qubit to prepare |1> state
    
    # Apply Hadamard gates to all qubits
    qc.h(range(n + 1))
    
    # Apply the oracle
    qc.append(oracle, range(n + 1))
    
    # Apply Hadamard gates to input qubits only
    qc.h(range(n))
    
    # Measure the input qubits
    qc.measure(range(n), range(n))
    
    # Use StatevectorSampler to get the final state before measurement
    sampler = StatevectorSampler()
    job = sampler.run(qc, shots=1)
    result = job.result()
    
    # Get the statevector (only first sample since we're using 1 shot)
    statevector = result[0].data
    
    # Check if the first amplitude (|0...0> state) has probability ~1
    # For constant function, measurement should give all zeros with probability 1
    prob_zero = abs(statevector[0]) ** 2
    
    return isclose(prob_zero, 1.0, atol=1e-8)
