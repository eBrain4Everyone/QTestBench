# LLM-generated solution — task_0034
# Generated: 2026-06-23T18:30:33.922239
# Model: gemini3pro
# Variant: generated_rag_1

from qiskit_ibm_runtime import Batch, Sampler, SamplerV2
from qiskit.primitives.primitive_job import PrimitiveJob
from qiskit_ibm_runtime.fake_provider import FakeAlgiers
from qiskit.transpiler import CouplingMap
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

def run_jobs_on_batch() -> dict:
    """ 
    Generate all four Bell states and execute them on the FakeAlgiers backend using SamplerV2 with batch mode. 
    Each Bell state circuit will be transpiled with an optimization level of 3, with the seed 123 for the transpiler.
    Returns a dictionary where the keys are the Bell state names ['phi_plus', 'phi_minus', 'psi_plus', 'psi_minus'] 
    and the values are the corresponding RuntimeJob objects and the batch id.
    """
    backend = FakeAlgiers()
    pm = generate_preset_pass_manager(optimization_level=3, backend=backend, seed_transpiler=123)
    
    # 1. phi_plus: |00> + |11>
    qc_phi_plus = QuantumCircuit(2)
    qc_phi_plus.h(0)
    qc_phi_plus.cx(0, 1)
    qc_phi_plus.measure_all()
    
    # 2. phi_minus: |00> - |11>
    qc_phi_minus = QuantumCircuit(2)
    qc_phi_minus.x(0)
    qc_phi_minus.h(0)
    qc_phi_minus.cx(0, 1)
    qc_phi_minus.measure_all()
    
    # 3. psi_plus: |01> + |10>
    qc_psi_plus = QuantumCircuit(2)
    qc_psi_plus.x(1)
    qc_psi_plus.h(0)
    qc_psi_plus.cx(0, 1)
    qc_psi_plus.measure_all()
    
    # 4. psi_minus: |01> - |10>
    qc_psi_minus = QuantumCircuit(2)
    qc_psi_minus.x(0)
    qc_psi_minus.x(1)
    qc_psi_minus.h(0)
    qc_psi_minus.cx(0, 1)
    qc_psi_minus.measure_all()
    
    # Transpile the circuits
    isa_phi_plus = pm.run(qc_phi_plus)
    isa_phi_minus = pm.run(qc_phi_minus)
    isa_psi_plus = pm.run(qc_psi_plus)
    isa_psi_minus = pm.run(qc_psi_minus)
    
    # Execute in Batch mode using SamplerV2
    with Batch(backend=backend) as batch:
        sampler = SamplerV2(mode=batch)
        job_phi_plus = sampler.run([isa_phi_plus])
        job_phi_minus = sampler.run([isa_phi_minus])
        job_psi_plus = sampler.run([isa_psi_plus])
        job_psi_minus = sampler.run([isa_psi_minus])
        
        batch_id = batch.session_id
        
    return {
        'phi_plus': job_phi_plus,
        'phi_minus': job_phi_minus,
        'psi_plus': job_psi_plus,
        'psi_minus': job_psi_minus,
        'batch_id': batch_id
    }
