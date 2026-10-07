# LLM-generated solution — task_0001
# Generated: 2026-06-23T18:48:08.428965
# Model: qwen3
# Variant: generated_non_rag_2

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

def run_bell_state_simulator():
    """ Define a phi plus bell state using Qiskit, transpile the circuit using pass manager with optimization level as 1, run it using Qiskit Sampler with the Aer simulator as backend and return the counts dictionary.
    """
    # Create a Bell state circuit: |_+_ = (|00_ + |11_)/_2
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    
    # Set up the Aer simulator backend
    backend = AerSimulator()
    
    # Generate a pass manager with optimization level 1
    pass_manager = generate_preset_pass_manager(optimization_level=1, backend=backend)
    
    # Transpile the circuit
    transpiled_qc = pass_manager.run(qc)
    
    # Create a Sampler instance
    sampler = Sampler(backend=backend)
    
    # Run the sampler and get result
    job = sampler.run(transpiled_qc)
    result = job.result()
    
    # Extract counts from the result
    # The result is a list of QuasiDist objects, we need to get the first one
    # and convert to counts (dictionaries with bitstrings as keys and counts as values)
    # Since we're using AerSimulator, we can get counts directly
    # For Sampler, the result contains 'quasi_dists' and 'metadata'
    # We'll use the first circuit's result
    
    # Convert quasi-distribution to counts dictionary
    # Since we used measurement, we expect binary outcomes
    quasi_dist = result[0].quasi_dists[0]
    
    # Convert to integer counts (scale by 1024 shots by default for Sampler)
    # But we need to get actual shot count
    shots = result[0].metadata.get('shots', 1024)
    
    # Create counts dictionary with integer keys converted to bitstrings
    counts = {}
    for key, probability in quasi_dist.items():
        # Convert integer key to bitstring with appropriate length
        bitstring = format(key, f'0{transpiled_qc.num_qubits()}b')
        # Approximate count as probability * shots, rounded to integer
        count = round(probability * shots)
        counts[bitstring] = count
    
    return counts
