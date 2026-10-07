# LLM-generated solution — task_0035
# Generated: 2026-06-23T18:46:15.919563
# Model: gpt54
# Variant: generated_non_rag_1

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
    circuit.measure_all()

    observable = SparsePauliOp.from_list([("IIIIZ", 1.0)])

    pm = generate_preset_pass_manager(
        optimization_level=1,
        backend=backend,
        seed_transpiler=789,
    )
    isa_circuit = pm.run(circuit)
    isa_observable = observable.apply_layout(isa_circuit.layout)

    options = EstimatorOptions()
    options.resilience_level = 0
    options.dynamical_decoupling.enable = True
    options.twirling.enable_gates = True

    estimator = Estimator(mode=backend, options=options)
    job = estimator.run([(isa_circuit, isa_observable, np.empty(0))])
    return job
