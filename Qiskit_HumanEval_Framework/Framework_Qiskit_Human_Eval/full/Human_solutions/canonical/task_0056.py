from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
def not_gate(a: int)->dict:
    """ Given an 8-bit integer, design a quantum circuit that acts as a classical NOT gate. Simulate the circuit Qiskit Sampler with the Aer simulator as backend and return the counts of the result.
    """

    circuit = QuantumCircuit(8)
    a = format(a, "08b")
    for i in range(8):
        if a[7-i] == "0":
            circuit.x(i)
    circuit.measure_all()
    backend = AerSimulator()
    sampler = Sampler(mode=backend)
    result = sampler.run([circuit]).result()
    return result[0].data.meas.get_counts()
