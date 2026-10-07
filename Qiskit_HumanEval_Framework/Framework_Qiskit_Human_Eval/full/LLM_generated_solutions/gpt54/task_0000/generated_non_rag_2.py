# LLM-generated solution — task_0000
# Generated: 2026-06-23T18:42:30.929778
# Model: gpt54
# Variant: generated_non_rag_2

from qiskit import QuantumCircuit

def create_quantum_circuit(n_qubits):
    """ Generate a Quantum Circuit for the given int 'n_qubits' and return it.
    """
    if not isinstance(n_qubits, int):
        raise TypeError("n_qubits must be an integer")
    if n_qubits < 0:
        raise ValueError("n_qubits must be non-negative")

    qc = QuantumCircuit(n_qubits)

    if n_qubits == 0:
        return qc

    for i in range(n_qubits):
        qc.h(i)

    for i in range(n_qubits - 1):
        qc.cx(i, i + 1)

    return qc
