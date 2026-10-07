from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
def random_number_generator_unsigned_8bit(n: int)->[int]:
    """ Write a function that generates n number of random 8-bit unsigned integers using a Quantum Circuit and outputs a list of integers.
    """

    circuit = QuantumCircuit(8)
    circuit.h(range(8))
    circuit.measure_all()
    backend = AerSimulator()
    sampler = Sampler(mode=backend)
    result = sampler.run([circuit], shots=n).result()
    samples = result[0].data.meas.get_bitstrings()
    return [int(sample, 2) for sample in samples]
