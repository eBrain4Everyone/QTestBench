# LLM-generated solution — task_0000
# Generated: 2026-06-23T18:02:02.148991
# Model: deepseekv32
# Variant: generated_non_rag_2

from qiskit import QuantumCircuit
def create_quantum_circuit(n_qubits):
    """ Generate a Quantum Circuit for the given int 'n_qubits' and return it.
    """
    qc = QuantumCircuit(n_qubits)
    for i in range(n_qubits):
        qc.h(i)
    for i in range(n_qubits-1):
        qc.cx(i, i+1)
    return qc
