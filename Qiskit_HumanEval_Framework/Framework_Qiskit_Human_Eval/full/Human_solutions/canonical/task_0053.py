from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
from qiskit.circuit.library import XOR
def xor_gate(a: int, b: int)->dict:
    """ Given two 8-bit integers a and b design a Quantum Circuit that acts as a classical XOR gate. Simulate the circuit using Qiskit Sampler with the Aer simulator as backend and return the counts of the result.
    """

    circuit = XOR(8, a).compose(XOR(8, b))
    circuit.measure_all()
    backend = AerSimulator()
    sampler = Sampler(mode=backend)
    result = sampler.run([circuit.decompose()]).result()
    return result[0].data.meas.get_counts()
