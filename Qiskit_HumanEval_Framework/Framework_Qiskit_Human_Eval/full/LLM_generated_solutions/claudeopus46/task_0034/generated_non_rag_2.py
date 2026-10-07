# LLM-generated solution — task_0034
# Generated: 2026-06-23T17:59:08.014910
# Model: claudeopus46
# Variant: generated_non_rag_2

from qiskit_ibm_runtime import Batch, SamplerV2 as Sampler
from qiskit.primitives.primitive_job import PrimitiveJob
from qiskit_ibm_runtime.fake_provider import FakeAlgiers
from qiskit.transpiler import CouplingMap
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager


def run_jobs_on_batch() -> dict:
    """Generate all four Bell states and execute them on the FakeAlgiers backend using SamplerV2 with batch mode. Each Bell state circuit will be transpiled with an optimization level of 3, with the seed 123 for the transpiler.
    Returns a dictionary where the keys are the Bell state names ['phi_plus', 'phi_minus', 'psi_plus', 'psi_minus'] and the values are the corresponding RuntimeJob objects and the batch id.
    """
    backend = FakeAlgiers()

    # Create Bell state circuits
    # |_+_ = (|00_ + |11_) / _2
    phi_plus = QuantumCircuit(2)
    phi_plus.h(0)
    phi_plus.cx(0, 1)
    phi_plus.measure_all()

    # |_-_ = (|00_ - |11_) / _2
    phi_minus = QuantumCircuit(2)
    phi_minus.h(0)
    phi_minus.cx(0, 1)
    phi_minus.z(0)
    phi_minus.measure_all()

    # |_+_ = (|01_ + |10_) / _2
    psi_plus = QuantumCircuit(2)
    psi_plus.h(0)
    psi_plus.cx(0, 1)
    psi_plus.x(1)
    psi_plus.measure_all()

    # |_-_ = (|01_ - |10_) / _2
    psi_minus = QuantumCircuit(2)
    psi_minus.h(0)
    psi_minus.cx(0, 1)
    psi_minus.x(1)
    psi_minus.z(0)
    psi_minus.measure_all()

    circuits = {
        'phi_plus': phi_plus,
        'phi_minus': phi_minus,
        'psi_plus': psi_plus,
        'psi_minus': psi_minus,
    }

    # Transpile circuits
    pm = generate_preset_pass_manager(optimization_level=3, backend=backend, seed_transpiler=123)

    transpiled_circuits = {}
    for name, qc in circuits.items():
        transpiled_circuits[name] = pm.run(qc)

    # Run in batch mode
    result = {}
    with Batch(backend=backend) as batch:
        sampler = Sampler(mode=batch)
        for name, t_qc in transpiled_circuits.items():
            job = sampler.run([t_qc])
            result[name] = job
        batch_id = batch.session_id

    result['batch_id'] = batch_id

    return result
