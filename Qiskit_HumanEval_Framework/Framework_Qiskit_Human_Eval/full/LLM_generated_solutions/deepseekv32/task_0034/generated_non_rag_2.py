# LLM-generated solution — task_0034
# Generated: 2026-06-23T18:09:06.978125
# Model: deepseekv32
# Variant: generated_non_rag_2

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
    backend = FakeAlgiers()
    
    bell_states = {
        'phi_plus': QuantumCircuit(2),
        'phi_minus': QuantumCircuit(2),
        'psi_plus': QuantumCircuit(2),
        'psi_minus': QuantumCircuit(2)
    }
    
    bell_states['phi_plus'].h(0)
    bell_states['phi_plus'].cx(0, 1)
    
    bell_states['phi_minus'].h(0)
    bell_states['phi_minus'].cx(0, 1)
    bell_states['phi_minus'].z(0)
    
    bell_states['psi_plus'].h(0)
    bell_states['psi_plus'].cx(0, 1)
    bell_states['psi_plus'].x(1)
    
    bell_states['psi_minus'].h(0)
    bell_states['psi_minus'].cx(0, 1)
    bell_states['psi_minus'].x(1)
    bell_states['psi_minus'].z(0)
    
    pm = generate_preset_pass_manager(backend=backend, optimization_level=3, seed_transpiler=123)
    
    transpiled_circuits = {}
    for name, circuit in bell_states.items():
        transpiled_circuits[name] = pm.run(circuit)
    
    sampler = Sampler(backend=backend)
    
    with Batch(backend=backend) as batch:
        jobs = {}
        for name, circuit in transpiled_circuits.items():
            job = sampler.run([circuit])
            jobs[name] = job
        
        batch_id = batch.batch_id()
    
    result = {}
    for name in bell_states.keys():
        result[name] = {
            'job': jobs[name],
            'batch_id': batch_id
        }
    
    return result
