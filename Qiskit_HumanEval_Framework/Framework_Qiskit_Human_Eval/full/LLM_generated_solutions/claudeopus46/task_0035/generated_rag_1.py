# LLM-generated solution — task_0035
# Generated: 2026-06-23T18:00:46.248855
# Model: claudeopus46
# Variant: generated_rag_1

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
    circuit = EfficientSU2(num_qubits=5, reps=2, entanglement="pairwise")

    # Assign random parameters (or use default values)
    num_params = circuit.num_parameters
    np.random.seed(42)
    param_values = np.random.uniform(0, 2 * np.pi, num_params)
    circuit.assign_parameters(param_values, inplace=True)

    # Transpile the circuit
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend, seed_transpiler=789)
    transpiled_circuit = pm.run(circuit)

    # Create observable: 1*Z on the last qubit (Z_-1 means Z on qubit index num_qubits-1)
    # For 5 qubits, Z on the last qubit (index 4) is "IIIII" with Z at position -1
    # In SparsePauliOp notation, the rightmost character is qubit 0, so Z on qubit 4 is "ZIIIII"... 
    # Actually for 5 qubits: qubit 4 (last) -> "ZIIII"
    # But after transpilation the number of qubits might change to match the backend layout
    # We need to use the transpiled circuit's num_qubits
    n_qubits = transpiled_circuit.num_qubits
    # Z on the last qubit (index n_qubits - 1): in Pauli string, leftmost char = highest index qubit
    pauli_str = "Z" + "I" * (n_qubits - 1)
    observable = SparsePauliOp(pauli_str, coeffs=[1.0])

    # Set up EstimatorOptions with dynamical decoupling and T-REx
    options = EstimatorOptions()

    # Enable dynamical decoupling
    options.dynamical_decoupling.enable = True
    options.dynamical_decoupling.sequence_type = "XpXm"

    # Enable T-REx (Twirled Readout Error eXtinction) resilience
    options.resilience.measure_mitigation = True
    options.resilience.zne_mitigation = False
    options.twirling.enable_gates = True
    options.twirling.enable_measure = True

    # Create Estimator with the backend and options
    estimator = Estimator(backend=backend, options=options)

    # Run the estimation
    job = estimator.run([(transpiled_circuit, observable)])

    return job
