# LLM-generated solution — task_0000
# Generated: 2026-06-23T18:42:36.580854
# Model: gpt54
# Variant: generated_non_rag_3

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

    qc.h(0)
    for i in range(1, n_qubits):
        qc.cx(i - 1, i)

    return qc
