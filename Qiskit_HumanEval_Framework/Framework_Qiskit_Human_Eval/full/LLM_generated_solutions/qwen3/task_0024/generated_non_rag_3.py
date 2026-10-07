# LLM-generated solution — task_0024
# Generated: 2026-06-23T18:51:23.377102
# Model: qwen3
# Variant: generated_non_rag_3

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from numpy import isclose
from qiskit.quantum_info import Statevector

def dj_algorithm(oracle: QuantumCircuit) -> bool:
    """ Given a Deutsch-Jozsa oracle in which the final qubit is the "output" qubit, return True if the oracle is constant or False otherwise.
    """
    n = oracle.num_qubits - 1  # Number of input qubits (output qubit is the last one)
    
    # Create the Deutsch-Jozsa circuit
    dj_circuit = QuantumCircuit(n + 1)
    
    # Initialize the input qubits in |+> state and output qubit in |1> state
    for i in range(n):
        dj_circuit.h(i)
    dj_circuit.x(n)  # Put output qubit in |1> state
    
    # Apply the oracle
    dj_circuit.append(oracle, range(n + 1))
    
    # Apply Hadamard gates to input qubits again
    for i in range(n):
        dj_circuit.h(i)
    
    # Measure the input qubits
    dj_circuit.measure_all()
    
    # Use StatevectorSampler to get the state before measurement
    sampler = StatevectorSampler()
    job = sampler.run([dj_circuit], shots=1)
    result = job.result()
    
    # Get the statevector (the result should have only one non-zero amplitude for the measurement outcome)
    state = result[0].data[0]
    
    # Check if the first amplitude (|0...0>) is non-zero
    # In the DJ algorithm, if the oracle is constant, measuring |0...0> is guaranteed
    # If the oracle is balanced, measuring |0...0> has probability 0
    zero_state_index = 0  # Index for |0...0> state
    
    # Since we're only interested in whether we get all zeros, check the amplitude for |0...0> followed by |0> (output qubit)
    # But actually, after the second H-gate transformation on the input qubits, the output qubit doesn't matter for measurement
    # We only care about the input qubits being all zeros
    
    # The statevector has dimension 2^(n+1), with the last qubit being the output
    # We want to check if the amplitude for the input qubits being |0...0> is non-zero
    # This corresponds to amplitudes at indices where the first n qubits are 0
    # For n qubits, this is indices 0 and 1 (if output qubit is |0> and |1> respectively)
    
    # Sum the probabilities for |0...0> followed by |0> and |0...0> followed by |1>
    prob_zero = abs(state[0])**2 + abs(state[1])**2
    
    # If the oracle is constant, we should measure |0...0> with probability 1
    # So prob_zero should be 1 (or very close to 1)
    return isclose(prob_zero, 1.0, atol=1e-10)
