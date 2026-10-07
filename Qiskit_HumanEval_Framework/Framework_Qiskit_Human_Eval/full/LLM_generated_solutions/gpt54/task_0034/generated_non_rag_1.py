# LLM-generated solution — task_0034
# Generated: 2026-06-23T18:45:31.358792
# Model: gpt54
# Variant: generated_non_rag_1

from qiskit_ibm_runtime import Batch, Sampler
from qiskit.primitives.primitive_job import PrimitiveJob
from qiskit_ibm_runtime.fake_provider import FakeAlgiers
from qiskit.transpiler import CouplingMap
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager


def run_jobs_on_batch() -> dict:
    backend = FakeAlgiers()
    coupling_map = CouplingMap(backend.configuration().coupling_map)

    def bell_circuit(name: str) -> QuantumCircuit:
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        if name == "phi_minus":
            qc.z(0)
        elif name == "psi_plus":
            qc.x(1)
        elif name == "psi_minus":
            qc.x(1)
            qc.z(0)
        qc.measure_all()
        return qc

    bell_names = ["phi_plus", "phi_minus", "psi_plus", "psi_minus"]
    circuits = {name: bell_circuit(name) for name in bell_names}

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
        for name in bell_names:
            job = sampler.run([transpiled[name]])
            results[name] = job
        results["batch_id"] = batch.session_id

    return results
