from typing import List
from qiskit.circuit.random import random_circuit
from qiskit_ibm_runtime import Sampler, SamplerOptions
from qiskit_aer import AerSimulator
def run_multiple_sampler() -> List:
    """ Generate two random quantum circuits, each with 2 qubits and a depth of 2, using seed values of 0 and 1 respectively. Run the circuits using the Sampler on the Aer simulator with the seed set as 42 and return the counts for both circuits.
    """

    circuits = (
        random_circuit(2, 2, seed=0, measure=True).decompose(reps=1),
        random_circuit(2, 2, seed=1, measure=True).decompose(reps=1),
    )
    options = SamplerOptions()
    options.simulator.seed_simulator=42
    sampler = Sampler(mode=AerSimulator(), options=options)
    job = sampler.run(circuits)
    results = job.result()
    statevectors = [result.data.c.get_counts() for result in results]
    return statevectors
