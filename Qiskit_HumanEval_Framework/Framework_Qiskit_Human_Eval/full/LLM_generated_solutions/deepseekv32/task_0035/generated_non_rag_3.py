# LLM-generated solution — task_0035
# Generated: 2026-06-23T18:11:09.658493
# Model: deepseekv32
# Variant: generated_non_rag_3

from qiskit.circuit.library import efficient_su2
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler import CouplingMap
import numpy as np
from qiskit_ibm_runtime import Estimator, EstimatorOptions
from qiskit.primitives.primitive_job import PrimitiveJob
from qiskit_ibm_runtime.fake_provider import FakeAuckland
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit import transpile
from qiskit_aer import AerSimulator

def run_circuit_with_dd_trex() -> PrimitiveJob:
    """
    Run an EfficientSU2 circuit with 5 qubits, 2 repetitions, and pairwise entanglement on the FakeAuckland backend.
    The circuit should be transpiled with an optimization level of 1 and a transpiler seed of 789. Use 1*Z_-1 observable to calculate the expectation value.
    """
    # Create EfficientSU2 circuit
    circuit = efficient_su2(num_qubits=5, reps=2, entanglement='pairwise')
    
    # Create observable: 1*Z on last qubit (index -1)
    observable = SparsePauliOp.from_list([('Z' + 'I' * 4, 1.0)])
    
    # Get FakeAuckland backend
    backend = FakeAuckland()
    
    # Generate transpiled circuit with optimization level 1 and seed 789
    pass_manager = generate_preset_pass_manager(
        backend=backend,
        optimization_level=1,
        seed_transpiler=789
    )
    transpiled_circuit = pass_manager.run(circuit)
    
    # Create Estimator with appropriate options
    options = EstimatorOptions(
        default_shots=1024,
        simulator=backend
    )
    
    # Create Estimator instance
    estimator = Estimator(session=None, options=options)
    
    # Run the job
    job = estimator.run(circuits=transpiled_circuit, observables=observable)
    
    return job
