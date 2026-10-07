from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
def random_coin_flip(samples: int)->dict:
    """ Design a Quantum Circuit that simulates random coin flips for the given samples using Qiskit Sampler with the Aer simulator as backend and outputs the count of heads and tails in a dictionary. The heads should be stored in the dict as 'Heads' and tails as 'Tails'. For example
    random_coin_flip(10) == {'Heads' : 5, 'Tails : 5}
    random_coin_flip(20) == {'Heads' : 9, 'Tails : 11}.
    """

    circuit = QuantumCircuit(1,1)
    circuit.h(0)
    circuit.measure_all()
    backend = AerSimulator()
    sampler = Sampler(mode=backend)
    result = sampler.run([circuit], shots=samples).result()
    counts = result[0].data.meas.get_counts()
    return {'Heads' : counts['0'], 'Tails': counts['1']}
