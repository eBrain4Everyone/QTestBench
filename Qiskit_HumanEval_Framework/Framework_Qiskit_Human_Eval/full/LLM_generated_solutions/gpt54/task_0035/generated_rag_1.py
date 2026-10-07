# LLM-generated solution — task_0035
# Generated: 2026-06-23T18:46:41.534728
# Model: gpt54
# Variant: generated_rag_1

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
    param_values = rng.random(circuit.num_parameters)

    observable = SparsePauliOp.from_list([("IIIIZ", 1.0)])

    _ = CouplingMap(backend.configuration().coupling_map)

    pm = generate_preset_pass_manager(
        optimization_level=1,
        backend=backend,
        seed_transpiler=789,
    )
    isa_circuit = pm.run(circuit)
    isa_observable = observable.apply_layout(isa_circuit.layout)

    options = EstimatorOptions()
    if hasattr(options, "dynamical_decoupling"):
        options.dynamical_decoupling.enable = True
    if hasattr(options, "twirling"):
        if hasattr(options.twirling, "enable_measure"):
            options.twirling.enable_measure = True
        elif hasattr(options.twirling, "enable"):
            options.twirling.enable = True
    if hasattr(options, "resilience"):
        if hasattr(options.resilience, "measure_mitigation"):
            options.resilience.measure_mitigation = True
        if hasattr(options.resilience, "zne_mitigation"):
            options.resilience.zne_mitigation = False

    estimator = Estimator(mode=backend, options=options)
    return estimator.run([(isa_circuit, isa_observable, param_values)])
