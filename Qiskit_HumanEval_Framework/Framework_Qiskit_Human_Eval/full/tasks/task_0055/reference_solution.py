from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
def or_gate(a: int, b: int)->dict:
    """ Given two 3-bit integers a and b, design a quantum circuit that acts as a classical OR gate. Simulate the circuit using Qiskit Sampler with the Aer simulator as backend and return the counts of the result.
    """

    qr_a = QuantumRegister(3, "qr_a")
    qr_b = QuantumRegister(3, "qr_b")
    ancillary = QuantumRegister(3, "ancillary")
    measure = ClassicalRegister(3, "measure")
    circuit = QuantumCircuit(qr_a, qr_b, ancillary, measure)
    a = format(a, '03b')
    b = format(b, '03b')
    for i in range(3):
        if a[2-i] == '0':
            circuit.x(qr_a[i])
        if b[2-i] == '0':
            circuit.x(qr_b[i])
    for i in range(3):
        circuit.ccx(qr_a[i], qr_b[i], ancillary[i])
    circuit.x(ancillary)
    circuit.measure(ancillary, measure)
    backend = AerSimulator()
    sampler = Sampler(mode=backend)
    result = sampler.run([circuit]).result()
    return result[0].data.measure.get_counts()
