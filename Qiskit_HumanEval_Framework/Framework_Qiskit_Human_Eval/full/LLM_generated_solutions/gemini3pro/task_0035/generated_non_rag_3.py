# LLM-generated solution — task_0035
# Generated: 2026-06-23T18:36:03.880460
# Model: gemini3pro
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
    # 1. Create the parameterized circuit
    circuit = EfficientSU2(num_qubits=5, reps=2, entanglement='pairwise')
    
    # 2. Transpile the circuit
    backend = FakeAuckland()
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend, seed_transpiler=789)
    isa_circuit = pm.run(circuit)
    
    # 3. Create the observable and apply layout
    # 1*Z_-1 means Z on the last qubit (index 4 for 5 qubits)
    obs = SparsePauliOp.from_sparse_list([("Z", [4], 1.0)], num_qubits=5)
    isa_obs = obs.apply_layout(isa_circuit.layout)
    
    # 4. Bind parameters (using zeros as defaults)
    param_values = np.zeros(circuit.num_parameters)
    
    # 5. Set Estimator options for DD and TREX
    options = EstimatorOptions()
    if hasattr(options, "resilience_level"):
        options.resilience_level = 1
    if hasattr(options, "dynamical_decoupling"):
        options.dynamical_decoupling.enable = True

    # 6. Initialize Estimator and run
    estimator = Estimator(backend=backend, options=options)
    
    # Try V2 API first, fallback to V1 if necessary
    try:
        job = estimator.run([(isa_circuit, isa_obs, param_values)])
    except Exception:
        # Fallback for V1 API
        if hasattr(options, "transpilation"):
            options.transpilation.skip_transpilation = True
        estimator = Estimator(backend=backend, options=options)
        job = estimator.run(circuits=[isa_circuit], observables=[isa_obs], parameter_values=[param_values])
        
    return job
