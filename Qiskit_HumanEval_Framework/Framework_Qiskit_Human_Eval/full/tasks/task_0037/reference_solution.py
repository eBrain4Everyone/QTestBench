from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
from qiskit.primitives.containers.primitive_result import PrimitiveResult
def bv_algorithm(s: str) -> [list, PrimitiveResult]:
    """ Illustrate a Bernstein-Vazirani algorithm routine on Qiskit and run it using Qiskit Sampler with Aer simulator as backend for a string of 0s and 1s. Return the bit strings of the result and the result itself.
    """

    qc = QuantumCircuit(len(s) + 1)
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            qc.cx(index, len(s))
    qc.measure_all()
    backend = AerSimulator()
    sampler = Sampler(mode=backend)
    result= sampler.run([qc], shots=1).result()
    bitstrings = result[0].data.meas.get_bitstrings()
    return [bitstrings, result]
