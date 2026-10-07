from qiskit import QuantumCircuit
def bv_function(s: str) -> QuantumCircuit:
    """ Write a function to design a Bernstein-Vazirani oracle from a bitstring and return it.
    """

    n = len(s)
    qc = QuantumCircuit(n + 1)
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            qc.cx(index, n)
    return qc
