# LLM-generated solution — task_0034
# Generated: 2026-06-23T18:09:36.954633
# Model: deepseekv32
# Variant: generated_non_rag_3

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
    # Create the four Bell state circuits
    bell_states = {}
    
    # phi_plus: (|00> + |11>)/_2
    phi_plus = QuantumCircuit(2, 2)
    phi_plus.h(0)
    phi_plus.cx(0, 1)
    bell_states['phi_plus'] = phi_plus
    
    # phi_minus: (|00> - |11>)/_2
    phi_minus = QuantumCircuit(2, 2)
    phi_minus.h(0)
    phi_minus.cx(0, 1)
    phi_minus.z(0)
    bell_states['phi_minus'] = phi_minus
    
    # psi_plus: (|01> + |10>)/_2
    psi_plus = QuantumCircuit(2, 2)
    psi_plus.h(0)
    psi_plus.cx(0, 1)
    psi_plus.x(1)
    bell_states['psi_plus'] = psi_plus
    
    # psi_minus: (|01> - |10>)/_2
    psi_minus = QuantumCircuit(2, 2)
    psi_minus.h(0)
    psi_minus.cx(0, 1)
    psi_minus.x(1)
    psi_minus.z(0)
    bell_states['psi_minus'] = psi_minus
    
    # Create fake backend
    fake_backend = FakeAlgiers()
    
    # Generate pass manager with optimization level 3 and seed 123
    pass_manager = generate_preset_pass_manager(
        optimization_level=3,
        backend=fake_backend,
        seed_transpiler=123
    )
    
    # Transpile all circuits
    transpiled_circuits = {}
    for name, circuit in bell_states.items():
        transpiled_circuits[name] = pass_manager.run(circuit)
    
    # Create batch and submit jobs
    with Batch(backend=fake_backend) as batch:
        # Create Sampler instance
        sampler = Sampler()
        
        # Submit jobs for each circuit
        jobs = {}
        for name, circuit in transpiled_circuits.items():
            job = sampler.run([circuit])
            jobs[name] = job
        
        # Get batch id
        batch_id = batch.batch_id
    
    # Create result dictionary
    result = {}
    for name in bell_states.keys():
        result[name] = {
            'job': jobs[name],
            'batch_id': batch_id
        }
    
    return result
