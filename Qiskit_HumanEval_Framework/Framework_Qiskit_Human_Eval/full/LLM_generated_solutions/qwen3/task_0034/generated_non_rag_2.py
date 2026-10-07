# LLM-generated solution — task_0034
# Generated: 2026-06-23T18:51:51.232979
# Model: qwen3
# Variant: generated_non_rag_2

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
    # Define the backend
    backend = FakeAlgiers()
    
    # Create the circuits for the four Bell states
    bell_states = {}
    
    # Phi+ = (|00_ + |11_)/_2
    qc_phi_plus = QuantumCircuit(2)
    qc_phi_plus.h(0)
    qc_phi_plus.cx(0, 1)
    bell_states['phi_plus'] = qc_phi_plus
    
    # Phi- = (|00_ - |11_)/_2
    qc_phi_minus = QuantumCircuit(2)
    qc_phi_minus.h(0)
    qc_phi_minus.cx(0, 1)
    qc_phi_minus.z(0)
    bell_states['phi_minus'] = qc_phi_minus
    
    # Psi+ = (|01_ + |10_)/_2
    qc_psi_plus = QuantumCircuit(2)
    qc_psi_plus.x(1)
    qc_psi_plus.h(0)
    qc_psi_plus.cx(0, 1)
    bell_states['psi_plus'] = qc_psi_plus
    
    # Psi- = (|01_ - |10_)/_2
    qc_psi_minus = QuantumCircuit(2)
    qc_psi_minus.x(1)
    qc_psi_minus.h(0)
    qc_psi_minus.cx(0, 1)
    qc_psi_minus.z(0)
    bell_states['psi_minus'] = qc_psi_minus
    
    # Set up transpiler with optimization level 3 and seed 123
    pass_manager = generate_preset_pass_manager(optimization_level=3, backend=backend, seed_transpiler=123)
    
    # Transpile all circuits
    transpiled_circuits = {}
    for name, circuit in bell_states.items():
        transpiled_circuits[name] = pass_manager.run(circuit)
    
    # Create a batch and sampler
    batch = Batch(backend=backend)
    sampler = Sampler(mode=batch)
    
    # Store job and batch_id information
    results = {}
    
    # Submit all jobs in the batch
    for name, circuit in transpiled_circuits.items():
        job = sampler.run(circuit)
        results[name] = {
            'job': job,
            'batch_id': batch.batch_id
        }
    
    # Return the results dictionary
    return results
