# LLM-generated solution — task_0035
# Generated: 2026-06-23T18:34:17.413864
# Model: gemini3pro
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
    
    circuit = efficient_su2.EfficientSU2(5, reps=2, entanglement='pairwise')
    
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend, seed_transpiler=789)
    isa_circuit = pm.run(circuit)
    
    observable = SparsePauliOp.from_list([("ZIIII", 1.0)])
    isa_observable = observable.apply_layout(isa_circuit.layout)
    
    params = np.zeros(circuit.num_parameters)
    
    try:
        options = EstimatorOptions()
        options.dynamical_decoupling.enable = True
        options.resilience.measure_mitigation = True
        estimator = Estimator(mode=backend, options=options)
        is_v2 = True
    except TypeError:
        is_v2 = False

    if is_v2:
        job = estimator.run([(isa_circuit, isa_observable, params)])
    else:
        options_dict = {
            "skip_transpilation": True,
            "resilience_level": 1,
            "advanced_options": {
                "dynamical_decoupling": {"enable": True}
            }
        }
        estimator = Estimator(backend=backend, options=options_dict)
        job = estimator.run([isa_circuit], [isa_observable], [params])
        
    return job
