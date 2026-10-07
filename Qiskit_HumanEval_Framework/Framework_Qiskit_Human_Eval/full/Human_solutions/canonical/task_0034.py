from qiskit_ibm_runtime import Batch, Sampler
from qiskit.primitives.primitive_job import PrimitiveJob
from qiskit_ibm_runtime.fake_provider import FakeAlgiers
from qiskit.transpiler import CouplingMap
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
def run_jobs_on_batch() -> dict:
    """ Generate all four Bell states and execute them on the FakeAlgiers backend using SamplerV2 with batch mode. Each Bell state circuit will be transpiled with an optimization level of 3, with the seed 123 for the transpiler.
    Returns a dictionary where the keys are the Bell state names ['phi_plus', 'phi_minus', 'psi_plus', 'psi_minus'] and the values are the corresponding RuntimeJob objects and the batch id.
    """

    def create_bell_circuit(state):
        "Helper function to create bell state"
        qc = QuantumCircuit(2)
        qc.h(0) 
        qc.cx(0, 1)
        if state == "phi_minus":
            qc.z(0)
        elif state == "psi_plus":
            qc.x(1)
        elif state == "psi_minus":
            qc.x(1)
            qc.z(0)
        qc.measure_all()
        return qc
        
    # Create bell states
    bell_states = ["phi_plus", "phi_minus", "psi_plus", "psi_minus"]
    circuits = [create_bell_circuit(state) for state in bell_states]

    # Setting backend and pass managers
    backend = FakeAlgiers()
    coupling_map = CouplingMap(backend.configuration().coupling_map)
    pm = generate_preset_pass_manager(optimization_level = 3, backend=backend, seed_transpiler=123, coupling_map=coupling_map)

    # Running jobs using batch
    with Batch(backend=backend) as batch:
        jobs = {}
        sampler = Sampler(mode=batch)
        for bell_state, bell_circuit in zip(bell_states, circuits):
            isa_bell_circuit = pm.run(bell_circuit)
            jobs[bell_state] = sampler.run([(isa_bell_circuit)])
        return jobs
