# LLM-generated solution — task_0001
# Generated: 2026-06-23T18:48:44.487469
# Model: qwen3
# Variant: generated_rag_1

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

def run_bell_state_simulator():
    """ Define a phi plus bell state using Qiskit, transpile the circuit using pass manager with optimization level as 1, run it using Qiskit Sampler with the Aer simulator as backend and return the counts dictionary.
    """
    # Create Bell state (Phi+) circuit
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    
    # Initialize Aer simulator
    backend = AerSimulator()
    
    # Generate preset pass manager with optimization level 1
    pass_manager = generate_preset_pass_manager(optimization_level=1, backend=backend)
    
    # Transpile the circuit
    transpiled_qc = pass_manager.run(qc)
    
    # Create Sampler with the Aer backend
    sampler = Sampler(backend=backend)
    
    # Run the sampler
    job = sampler.run(transpiled_qc, shots=1024)
    result = job.result()
    
    # Extract counts dictionary
    counts = result.quasi_dists[0].binary_probabilities()
    
    return counts
