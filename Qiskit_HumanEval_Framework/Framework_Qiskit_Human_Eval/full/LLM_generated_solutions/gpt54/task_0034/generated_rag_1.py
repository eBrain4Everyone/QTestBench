# LLM-generated solution — task_0034
# Generated: 2026-06-23T18:46:04.263044
# Model: gpt54
# Variant: generated_rag_1

from qiskit_ibm_runtime import Batch, Sampler
from qiskit.primitives.primitive_job import PrimitiveJob
from qiskit_ibm_runtime.fake_provider import FakeAlgiers
from qiskit.transpiler import CouplingMap
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager


def run_jobs_on_batch() -> dict:
    """Generate all four Bell states and execute them on the FakeAlgiers backend using Sampler with batch mode.

    Each Bell state circuit is transpiled with optimization level 3 and seed 123.
    Returns a dictionary where the keys are the Bell state names and the values are the
    corresponding job objects, plus the batch id under key 'batch_id'.
    """
    backend = FakeAlgiers()
    coupling_map = CouplingMap(backend.configuration().coupling_map)

    circuits = {}

    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    circuits["phi_plus"] = qc

    qc = QuantumCircuit(2)
    qc.x(0)
    qc.h(0)
    qc.cx(0, 1)
    circuits["phi_minus"] = qc

    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.x(1)
    circuits["psi_plus"] = qc

    qc = QuantumCircuit(2)
    qc.x(0)
    qc.h(0)
    qc.cx(0, 1)
    qc.x(1)
    circuits["psi_minus"] = qc

    pm = generate_preset_pass_manager(
        optimization_level=3,
        backend=backend,
        coupling_map=coupling_map,
        seed_transpiler=123,
    )

    transpiled = {name: pm.run(circ) for name, circ in circuits.items()}

    results = {}
    with Batch(backend=backend) as batch:
        sampler = Sampler(mode=batch)
        for name, circuit in transpiled.items():
            try:
                job = sampler.run([circuit])
            except TypeError:
                job = sampler.run(circuit)
            results[name] = job
        results["batch_id"] = getattr(batch, "session_id", None) or getattr(batch, "batch_id", None)

    return results
