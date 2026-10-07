# LLM-generated solution — task_0024
# Generated: 2026-06-23T18:51:06.601857
# Model: qwen3
# Variant: generated_non_rag_1

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from numpy import isclose

def dj_algorithm(oracle: QuantumCircuit) -> bool:
    """ Given a Deutsch-Jozsa oracle in which the final qubit is the "output" qubit, return True if the oracle is constant or False otherwise.
    """
    n = oracle.num_qubits - 1  # number of input qubits
    circuit = QuantumCircuit(n + 1, n)
    
    # Initialize all input qubits to |+> and output qubit to |1>
    circuit.h(range(n))
    circuit.x(n)
    circuit.h(n)
    
    # Apply the oracle
    circuit.compose(oracle, inplace=True)
    
    # Apply Hadamard gates to input qubits again
    circuit.h(range(n))
    
    # Measure input qubits
    circuit.measure(range(n), range(n))
    
    # Use StatevectorSampler to get the statevector without measurement
    sampler = StatevectorSampler()
    result = sampler.run(circuit, shots=1).result()
    statevector = result[0].data.statevector
    
    # Check if the state is |0...0> for input qubits (meaning constant function)
    # The amplitude for |0...0, anything> should be 1 if constant
    # Since we don't care about output qubit, we trace it out or check specific indices
    # For DJ algorithm, if constant, input part should be |0...0> with amplitude _1
    
    # Get the amplitude for |0...00> and |0...01> (input all zeros, output 0 or 1)
    zero_input_idx_0 = 0  # |0...00>
    zero_input_idx_1 = 1  # |0...01>
    
    total_amplitude = abs(statevector[zero_input_idx_0])**2 + abs(statevector[zero_input_idx_1])**2
    
    # For constant function, this should be ~1, for balanced ~0
    return isclose(total_amplitude, 1.0, atol=1e-8)
