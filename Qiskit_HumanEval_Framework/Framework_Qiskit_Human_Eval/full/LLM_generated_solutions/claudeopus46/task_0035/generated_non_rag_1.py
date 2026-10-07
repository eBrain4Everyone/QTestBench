# LLM-generated solution — task_0035
# Generated: 2026-06-23T17:59:51.014604
# Model: claudeopus46
# Variant: generated_non_rag_1

from qiskit.circuit.library import EfficientSU2
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

    # Create the EfficientSU2 circuit
    circuit = EfficientSU2(num_qubits=5, reps=2, entanglement='pairwise')

    # Assign random parameters (or use default values)
    num_params = circuit.num_parameters
    np.random.seed(42)
    param_values = np.random.uniform(0, 2 * np.pi, num_params)
    circuit = circuit.assign_parameters(param_values)

    # Transpile the circuit
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend, seed_transpiler=789)
    transpiled_circuit = pm.run(circuit)

    # Create observable: 1*Z on the last qubit (index -1, i.e., qubit 4 for 5 qubits)
    # "Z_-1" means Z on the last qubit
    observable = SparsePauliOp.from_list([("IIIIZ", 1.0)])

    # Set up estimator options with dynamical decoupling and T-REx
    options = EstimatorOptions()
    options.dynamical_decoupling.enable = True
    options.dynamical_decoupling.sequence_type = "XpXm"
    options.resilience.measure_mitigation = True
    options.resilience_level = 1
    options.resilience.zne_mitigation = False
    options.twirling.enable_gates = True

    # Create estimator and run
    estimator = Estimator(backend=backend, options=options)
    job = estimator.run([(transpiled_circuit, observable)])

    return job
