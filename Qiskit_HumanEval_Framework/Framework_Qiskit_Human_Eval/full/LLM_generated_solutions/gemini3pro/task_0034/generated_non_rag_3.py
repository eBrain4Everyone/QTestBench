# LLM-generated solution — task_0034
# Generated: 2026-06-23T18:29:11.899808
# Model: gemini3pro
# Variant: generated_non_rag_3

from qiskit_ibm_runtime import Batch, Sampler, SamplerV2
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
    pm = generate_preset_pass_manager(optimization_level=3, backend=backend, seed_transpiler=123)
    
    bell_states = {}
    
    # phi_plus: |00> + |11>
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    bell_states['phi_plus'] = qc
    
    # phi_minus: |00> - |11>
    qc = QuantumCircuit(2)
    qc.x(0)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    bell_states['phi_minus'] = qc
    
    # psi_plus: |01> + |10>
    qc = QuantumCircuit(2)
    qc.x(1)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    bell_states['psi_plus'] = qc
    
    # psi_minus: |01> - |10>
    qc = QuantumCircuit(2)
    qc.x(0)
    qc.x(1)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    bell_states['psi_minus'] = qc
    
    result = {}
    
    with Batch(backend=backend) as batch:
        sampler = SamplerV2(mode=batch)
        for name, qc in bell_states.items():
            transpiled_qc = pm.run(qc)
            job = sampler.run([transpiled_qc])
            result[name] = job
            
        result['batch_id'] = batch.session_id
        
    return result
