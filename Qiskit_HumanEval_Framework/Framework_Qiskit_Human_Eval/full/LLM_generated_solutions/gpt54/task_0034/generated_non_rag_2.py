# LLM-generated solution — task_0034
# Generated: 2026-06-23T18:45:40.720457
# Model: gpt54
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
    coupling_map = CouplingMap(backend.configuration().coupling_map)

    circuits = {}

    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    circuits["phi_plus"] = qc

    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.z(0)
    qc.measure_all()
    circuits["phi_minus"] = qc

    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.x(1)
    qc.measure_all()
    circuits["psi_plus"] = qc

    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.x(1)
    qc.z(0)
    qc.measure_all()
    circuits["psi_minus"] = qc

    pm = generate_preset_pass_manager(
        optimization_level=3,
        backend=backend,
        coupling_map=coupling_map,
        seed_transpiler=123,
    )

    transpiled = {name: pm.run(circuit) for name, circuit in circuits.items()}

    results = {}
    with Batch(backend=backend) as batch:
        sampler = Sampler(mode=batch)
        for name in ["phi_plus", "phi_minus", "psi_plus", "psi_minus"]:
            job = sampler.run([transpiled[name]])
            results[name] = job
        results["batch_id"] = batch.session_id

    return results
