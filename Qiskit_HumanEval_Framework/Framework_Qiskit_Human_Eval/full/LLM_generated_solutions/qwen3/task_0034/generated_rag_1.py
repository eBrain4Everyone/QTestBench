# LLM-generated solution — task_0034
# Generated: 2026-06-23T18:52:08.752418
# Model: qwen3
# Variant: generated_rag_1

from qiskit_ibm_runtime import Batch, Sampler
from qiskit.primitives.primitive_job import PrimitiveJob
from qiskit_ibm_runtime.fake_provider import FakeAlgiers
from qiskit.transpiler import CouplingMap
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

def run_jobs_on_batch() -> dict:
    """ Generate all four Bell states and execute them on the FakeAlgiers backend using SamplerV2 with batch mode. Each Bell state circuit will be transpiled with an optimization level of 3, with the seed 123 for the transpiler.
    Returns a dictionary where the keys are the Bell state names ['phi_plus', 'phi_minus', 'psi_plus', 'psi_minus'] and the values are the corresponding RuntimeJob objects and the batch id.
    """
    # Create the four Bell states
    bell_states = {
        'phi_plus': QuantumCircuit(2),
        'phi_minus': QuantumCircuit(2),
        'psi_plus': QuantumCircuit(2),
        'psi_minus': QuantumCircuit(2)
    }
    
    # Build each Bell state circuit
    # |phi+> = (|00> + |11>)/sqrt(2)
    bell_states['phi_plus'].h(0)
    bell_states['phi_plus'].cx(0, 1)
    
    # |phi-> = (|00> - |11>)/sqrt(2)
    bell_states['phi_minus'].h(0)
    bell_states['phi_minus'].cx(0, 1)
    bell_states['phi_minus'].z(0)  # Add relative phase
    
    # |psi+> = (|01> + |10>)/sqrt(2)
    bell_states['psi_plus'].h(0)
    bell_states['psi_plus'].cx(0, 1)
    bell_states['psi_plus'].x(0)  # Transform to |01> + |10>
    
    # |psi-> = (|01> - |10>)/sqrt(2)
    bell_states['psi_minus'].h(0)
    bell_states['psi_minus'].cx(0, 1)
    bell_states['psi_minus'].x(0)
    bell_states['psi_minus'].z(0)  # Add relative phase
    
    # Initialize backend
    backend = FakeAlgiers()
    
    # Create transpiler pass manager with specified options
    pm = generate_preset_pass_manager(
        optimization_level=3,
        backend=backend,
        seed_transpiler=123
    )
    
    # Transpile all circuits
    transpiled_circuits = {}
    for name, circuit in bell_states.items():
        transpiled_circuits[name] = pm.run(circuit)
    
    # Create a batch and sampler
    batch = Batch(backend=backend)
    sampler = Sampler(mode=batch)
    
    # Submit jobs to the batch and store results
    results = {}
    for name, circuit in transpiled_circuits.items():
        job = sampler.run(circuit)
        results[name] = {
            'job': job,
            'batch_id': batch.id
        }
    
    # Return the results dictionary
    return results
