# LLM-generated solution — task_0035
# Generated: 2026-06-23T18:32:19.625569
# Model: gemini3pro
# Variant: generated_non_rag_1

from qiskit.circuit.library import efficient_su2, EfficientSU2
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
    # Initialize the backend
    backend = FakeAuckland()
    
    # Create the EfficientSU2 circuit
    circuit = EfficientSU2(num_qubits=5, reps=2, entanglement='pairwise')
    
    # Transpile the circuit
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend, seed_transpiler=789)
    isa_circuit = pm.run(circuit)
    
    # Define the 1*Z_-1 observable (Z on the last qubit, which is index 4)
    obs = SparsePauliOp.from_sparse_list([("Z", [4], 1.0)], num_qubits=5)
    
    # Map the observable to the physical layout
    isa_obs = obs.apply_layout(isa_circuit.layout)
    
    # Configure the Estimator options for Dynamical Decoupling (DD) and TREX (resilience_level=1)
    options = EstimatorOptions()
    options.resilience_level = 1
    options.dynamical_decoupling.enable = True
    
    # Initialize the Estimator
    estimator = Estimator(backend=backend, options=options)
    
    # Bind parameters with zeros
    param_values = np.zeros(isa_circuit.num_parameters)
    
    # Support both Estimator V2 (default in recent versions) and V1
    if getattr(estimator, "version", 1) == 2:
        job = estimator.run([(isa_circuit, isa_obs, param_values)])
    else:
        # Fallback for Estimator V1
        if hasattr(options, "transpilation"):
            options.transpilation.skip_transpilation = True
            estimator = Estimator(backend=backend, options=options)
        job = estimator.run(isa_circuit, isa_obs, parameter_values=[param_values])
        
    return job
