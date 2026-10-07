# LLM-generated solution — task_0035
# Generated: 2026-06-23T18:46:24.671693
# Model: gpt54
# Variant: generated_non_rag_2

from qiskit.circuit.library import efficient_su2
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler import CouplingMap
import numpy as np
from qiskit_ibm_runtime import Estimator, EstimatorOptions
from qiskit.primitives.primitive_job import PrimitiveJob
from qiskit_ibm_runtime.fake_provider import FakeAuckland
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager


def run_circuit_with_dd_trex() -> PrimitiveJob:
    """
    Run an EfficientSU2 circuit with 5 qubits, 2 repetitions, and pairwise entanglement on the FakeAuckland backend.
    The circuit should be transpiled with an optimization level of 1 and a transpiler seed of 789. Use 1*Z_-1 observable to calculate the expectation value.
    """
    backend = FakeAuckland()

    circuit = efficient_su2(
        num_qubits=5,
        reps=2,
        entanglement="pairwise",
    )
    rng = np.random.default_rng(789)
    params = rng.random(circuit.num_parameters)
    circuit = circuit.assign_parameters(params)

    try:
        observable = SparsePauliOp.from_list([("IIIIZ", 1.0)])
    except Exception:
        observable = SparsePauliOp.from_list([("Z", 1.0)])

    coupling_map = CouplingMap(backend.configuration().coupling_map)
    pm = generate_preset_pass_manager(
        optimization_level=1,
        backend=backend,
        coupling_map=coupling_map,
        seed_transpiler=789,
    )
    isa_circuit = pm.run(circuit)
    isa_observable = observable.apply_layout(isa_circuit.layout)

    options = EstimatorOptions()
    try:
        options.resilience.measure_mitigation = True
    except Exception:
        pass
    try:
        options.resilience.zne_mitigation = False
    except Exception:
        pass
    try:
        options.twirling.enable_gates = True
    except Exception:
        pass
    try:
        options.dynamical_decoupling.enable = True
    except Exception:
        pass

    estimator = Estimator(mode=backend, options=options)
    job = estimator.run([(isa_circuit, isa_observable)])
    return job
