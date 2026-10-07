# LLM-generated solution — task_0000
# Generated: 2026-06-23T18:42:40.374299
# Model: gpt54
# Variant: generated_rag_1

from qiskit import QuantumCircuit

def create_quantum_circuit(n_qubits):
    """Generate a QuantumCircuit with the given number of qubits and return it."""
    if not isinstance(n_qubits, int):
        raise TypeError("n_qubits must be an integer")
    if n_qubits < 0:
        raise ValueError("n_qubits must be non-negative")
    return QuantumCircuit(n_qubits)
