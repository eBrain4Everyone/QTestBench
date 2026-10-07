# LLM-generated solution — task_0001
# Generated: 2026-06-23T18:48:01.342260
# Model: qwen3
# Variant: generated_non_rag_1

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

def run_bell_state_simulator():
    """ Define a phi plus bell state using Qiskit, transpile the circuit using pass manager with optimization level as 1, run it using Qiskit Sampler with the Aer simulator as backend and return the counts dictionary.
    """
    # Create a Bell state circuit (|_+_ = (|00_ + |11_)/_2)
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    
    # Get the Aer simulator backend
    backend = AerSimulator()
    
    # Generate a preset pass manager with optimization level 1
    pass_manager = generate_preset_pass_manager(optimization_level=1, backend=backend)
    
    # Transpile the circuit
    transpiled_qc = pass_manager.run(qc)
    
    # Create a Sampler with the Aer backend
    sampler = Sampler(backend=backend)
    
    # Run the sampler and get results
    result = sampler.run(transpiled_qc).result()
    
    # Extract counts from the result
    # The result contains quasis for each circuit; we only have one circuit
    counts = result[0].metadata["counts"]
    
    return counts
