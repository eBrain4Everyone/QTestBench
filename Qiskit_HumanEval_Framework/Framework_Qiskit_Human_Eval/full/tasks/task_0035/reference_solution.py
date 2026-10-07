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

    n_qubits = 5
    reps = 2
    circuit = efficient_su2(n_qubits, entanglement="pairwise", reps=reps)
    observable = SparsePauliOp.from_sparse_list([("Z", [-1], 1.0)], num_qubits=n_qubits)
    

    # Generate random parameters
    rng = np.random.default_rng(1234)
    params = rng.uniform(-np.pi, np.pi, size=circuit.num_parameters)
    backend = FakeAuckland()
    coupling_map = CouplingMap(backend.configuration().coupling_map)
    pm = generate_preset_pass_manager(optimization_level = 1, backend=backend, seed_transpiler=789, coupling_map=coupling_map)
    isa_circuit = pm.run(circuit)
    isa_observable = observable.apply_layout(isa_circuit.layout)

    options = EstimatorOptions()
    options.environment.job_tags = ["run_circ_dd_trex"]
    estimator = Estimator(mode=backend, options=options)
    job = estimator.run([(isa_circuit, isa_observable, params)])
    return job
