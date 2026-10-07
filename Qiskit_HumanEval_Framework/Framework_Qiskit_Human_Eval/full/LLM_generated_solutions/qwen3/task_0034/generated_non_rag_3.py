# LLM-generated solution — task_0034
# Generated: 2026-06-23T18:51:59.659229
# Model: qwen3
# Variant: generated_non_rag_3

from qiskit_ibm_runtime import Batch, Sampler
from qiskit.primitives.primitive_job import PrimitiveJob
from qiskit_ibm_runtime.fake_provider import FakeAlgiers
from qiskit.transpiler import CouplingMap
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
import qiskit

def run_jobs_on_batch() -> dict:
    """ Generate all four Bell states and execute them on the FakeAlgiers backend using SamplerV2 with batch mode. Each Bell state circuit will be transpiled with an optimization level of 3, with the seed 123 for the transpiler.
    Returns a dictionary where the keys are the Bell state names ['phi_plus', 'phi_minus', 'psi_plus', 'psi_minus'] and the values are the corresponding RuntimeJob objects and the batch id.
    """
    # Define the four Bell states
    bell_circuits = {
        'phi_plus': QuantumCircuit(2),
        'phi_minus': QuantumCircuit(2),
        'psi_plus': QuantumCircuit(2),
        'psi_minus': QuantumCircuit(2)
    }
    
    # Prepare each Bell state
    bell_circuits['phi_plus'].h(0)
    bell_circuits['phi_plus'].cx(0, 1)
    bell_circuits['phi_plus'].measure_all()
    
    bell_circuits['phi_minus'].h(0)
    bell_circuits['phi_minus'].cx(0, 1)
    bell_circuits['phi_minus'].z(1)
    bell_circuits['phi_minus'].measure_all()
    
    bell_circuits['psi_plus'].h(0)
    bell_circuits['psi_plus'].cx(0, 1)
    bell_circuits['psi_plus'].x(1)
    bell_circuits['psi_plus'].measure_all()
    
    bell_circuits['psi_minus'].h(0)
    bell_circuits['psi_minus'].cx(0, 1)
    bell_circuits['psi_minus'].x(1)
    bell_circuits['psi_minus'].z(1)
    bell_circuits['psi_minus'].measure_all()
    
    # Load fake backend
    backend = FakeAlgiers()
    
    # Create transpilation pass manager with specified settings
    pm = generate_preset_pass_manager(
        optimization_level=3,
        backend=backend,
        seed_transpiler=123
    )
    
    # Transpile all circuits
    transpiled_circuits = {}
    for name, circuit in bell_circuits.items():
        transpiled_circuits[name] = pm.run(circuit)
    
    # Create batch
    batch = Batch(backend=backend)
    
    # Initialize sampler
    sampler = Sampler(mode=batch)
    
    # Execute each circuit in batch and store results
    jobs = {}
    for name, circuit in transpiled_circuits.items():
        job = sampler.run(circuit)
        jobs[name] = {'job': job, 'batch_id': batch.batch_id}
    
    # Return the dictionary with Bell state names as keys and job + batch_id as values
    return jobs
