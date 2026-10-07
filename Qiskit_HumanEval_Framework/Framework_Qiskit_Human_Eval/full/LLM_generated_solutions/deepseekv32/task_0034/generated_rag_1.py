# LLM-generated solution — task_0034
# Generated: 2026-06-23T18:10:13.285074
# Model: deepseekv32
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
    backend = FakeAlgiers()
    coupling_map = CouplingMap(backend.configuration().coupling_map)
    
    sampler = Sampler(backend=backend)
    
    bell_states = {}
    
    # phi_plus: (|00> + |11>)/_2
    qc_phi_plus = QuantumCircuit(2)
    qc_phi_plus.h(0)
    qc_phi_plus.cx(0, 1)
    
    # phi_minus: (|00> - |11>)/_2
    qc_phi_minus = QuantumCircuit(2)
    qc_phi_minus.h(0)
    qc_phi_minus.z(0)
    qc_phi_minus.cx(0, 1)
    
    # psi_plus: (|01> + |10>)/_2
    qc_psi_plus = QuantumCircuit(2)
    qc_psi_plus.h(0)
    qc_psi_plus.x(1)
    qc_psi_plus.cx(0, 1)
    
    # psi_minus: (|01> - |10>)/_2
    qc_psi_minus = QuantumCircuit(2)
    qc_psi_minus.h(0)
    qc_psi_minus.x(1)
    qc_psi_minus.z(0)
    qc_psi_minus.cx(0, 1)
    
    circuits = [qc_phi_plus, qc_phi_minus, qc_psi_plus, qc_psi_minus]
    names = ['phi_plus', 'phi_minus', 'psi_plus', 'psi_minus']
    
    pass_manager = generate_preset_pass_manager(
        optimization_level=3,
        backend=backend,
        seed_transpiler=123
    )
    
    transpiled_circuits = pass_manager.run(circuits)
    
    with Batch(sampler=sampler) as batch:
        jobs = []
        for circuit in transpiled_circuits:
            job = sampler.run([circuit])
            jobs.append(job)
        
        batch_id = batch.batch_id()
    
    result_dict = {}
    for name, job in zip(names, jobs):
        result_dict[name] = {
            'job': job,
            'batch_id': batch_id
        }
    
    return result_dict
