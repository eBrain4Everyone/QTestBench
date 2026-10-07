# LLM-generated solution — task_0035
# Generated: 2026-06-23T18:00:25.635206
# Model: claudeopus46
# Variant: generated_non_rag_3

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

    # Create EfficientSU2 circuit with 5 qubits, 2 reps, pairwise entanglement
    circuit = EfficientSU2(num_qubits=5, reps=2, entanglement='pairwise')

    # Assign random parameters (or use default values)
    num_params = circuit.num_parameters
    np.random.seed(42)
    param_values = np.random.uniform(0, 2 * np.pi, num_params)
    circuit = circuit.assign_parameters(param_values)

    # Transpile the circuit
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend, seed_transpiler=789)
    transpiled_circuit = pm.run(circuit)

    # Create observable: 1*Z on the last qubit (Z_-1 means qubit index -1, i.e., last qubit)
    # For 5 qubits, Z on the last qubit (qubit 4) is "IIIIZ" in Qiskit's convention
    # But in SparsePauliOp, the string is in little-endian, so Z on qubit 4 is "ZIIIII"... 
    # Actually for 5 qubits: qubit 0 is rightmost. Z_{-1} = Z on qubit 4 = "ZIIII"
    num_qubits = transpiled_circuit.num_qubits
    # Z on the last qubit (index -1, which is qubit num_original-1 = 4)
    # But after transpilation, the number of qubits might differ. 
    # The observable should match the transpiled circuit's qubits.
    # We need to use the original 5-qubit observable and let the estimator handle layout.
    # Actually, with the new Estimator from qiskit_ibm_runtime, we should pass the transpiled circuit
    # and an observable that matches.

    # "1*Z_-1" means Z on the last qubit of the original 5-qubit circuit
    # In SparsePauliOp for 5 qubits: Z on qubit 4 (last) = "ZIIII"
    observable = SparsePauliOp("ZIIII", coeffs=[1.0])

    # Apply the same layout to the observable
    observable = observable.apply_layout(transpiled_circuit.layout)

    # Set up estimator options with dynamical decoupling and T-REx
    options = EstimatorOptions()
    options.dynamical_decoupling.enable = True
    options.dynamical_decoupling.sequence_type = "XpXm"
    options.resilience.measure_mitigation = True
    options.resilience_level = 1  # T-REx

    estimator = Estimator(backend=backend, options=options)

    job = estimator.run([(transpiled_circuit, observable)])

    return job
