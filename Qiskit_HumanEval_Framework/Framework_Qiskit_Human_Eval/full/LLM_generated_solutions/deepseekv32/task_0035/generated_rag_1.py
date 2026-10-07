# LLM-generated solution — task_0035
# Generated: 2026-06-23T18:11:19.466039
# Model: deepseekv32
# Variant: generated_rag_1

from qiskit.circuit.library import efficient_su2
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler import CouplingMap
import numpy as np
from qiskit_ibm_runtime import Estimator, EstimatorOptions
from qiskit.primitives.primitive_job import PrimitiveJob
from qiskit_ibm_runtime.fake_provider import FakeAuckland
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit import QuantumCircuit

def run_circuit_with_dd_trex() -> PrimitiveJob:
    """
    Run an EfficientSU2 circuit with 5 qubits, 2 repetitions, and pairwise entanglement on the FakeAuckland backend.
    The circuit should be transpiled with an optimization level of 1 and a transpiler seed of 789. Use 1*Z_-1 observable to calculate the expectation value.
    """
    num_qubits = 5
    reps = 2
    entanglement = "pairwise"
    
    circuit = efficient_su2(num_qubits, reps=reps, entanglement=entanglement)
    
    backend = FakeAuckland()
    
    pm = generate_preset_pass_manager(
        optimization_level=1,
        backend=backend,
        seed_transpiler=789
    )
    
    transpiled_circuit = pm.run(circuit)
    
    observable = SparsePauliOp("Z" * (num_qubits - 1) + "I", coeffs=1.0)
    
    estimator = Estimator(
        backend=backend,
        options=EstimatorOptions(
            resilience_level=0,
            optimization_level=1
        )
    )
    
    job = estimator.run(transpiled_circuit, observable)
    
    return job
