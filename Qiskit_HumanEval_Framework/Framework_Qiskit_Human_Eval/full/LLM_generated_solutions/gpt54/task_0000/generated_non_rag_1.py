# LLM-generated solution — task_0000
# Generated: 2026-06-23T18:42:26.762129
# Model: gpt54
# Variant: generated_non_rag_1

from qiskit import QuantumCircuit

def create_quantum_circuit(n_qubits):
    """Generate a Quantum Circuit for the given int 'n_qubits' and return it."""
    if not isinstance(n_qubits, int):
        raise TypeError("n_qubits must be an integer")
    if n_qubits < 1:
        raise ValueError("n_qubits must be at least 1")

    qc = QuantumCircuit(n_qubits)

    for qubit in range(n_qubits):
        qc.h(qubit)

    for qubit in range(n_qubits - 1):
        qc.cx(qubit, qubit + 1)

    return qc
