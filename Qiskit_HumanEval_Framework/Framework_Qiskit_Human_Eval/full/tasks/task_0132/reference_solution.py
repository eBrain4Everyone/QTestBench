from qiskit.circuit.random import random_circuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import Batch, Sampler
from qiskit_ibm_runtime.fake_provider import FakeManilaV2
def run_batched_random_circuits():
    """ Generate 6 random quantum circuits, each with 3 qubits, depth of 2 and measure set to True; using the random_circuit Qiskit function, with seed 17. Then use a 
    preset pass manager to optimize these circuits with an optimization level of 1, the backend for the pass manager should be FakeManilaV2, and set the seed value 
    to 1. Partition these optimized circuits into batches of 3 circuits each, and execute these batches using Qiskit Runtime's Batch mode, and return a list containing 
    the measurement outcome for each batch. For the execution of each batch set the seed to 42 for the sampler primitive.
    """

    fake_manila = FakeManilaV2()
    pm = generate_preset_pass_manager(backend=fake_manila, optimization_level=1, seed_transpiler = 1)
    circuits = [pm.run(random_circuit(3, 2, measure=True, seed=17)) for _ in range(6)]
    batch_size = 3
    partitions = [circuits[i : i + batch_size] for i in range(0, len(circuits), batch_size)]
    sampler_options = {"simulator": {"seed_simulator": 42}}
    with Batch(backend=fake_manila):
        sampler = Sampler(mode=fake_manila, options=sampler_options)
        results = []
        for partition in partitions:
            job = sampler.run(partition)
            results.append(job.result()[0].data.c.get_counts())
    return results
