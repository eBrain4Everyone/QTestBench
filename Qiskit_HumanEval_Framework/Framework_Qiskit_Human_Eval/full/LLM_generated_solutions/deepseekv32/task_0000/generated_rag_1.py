# LLM-generated solution — task_0000
# Generated: 2026-06-23T18:02:25.770037
# Model: deepseekv32
# Variant: generated_rag_1

from qiskit import QuantumCircuit
def create_quantum_circuit(n_qubits):
    """ Generate a Quantum Circuit for the given int 'n_qubits' and return it.
    """
    qc = QuantumCircuit(n_qubits)
    for i in range(n_qubits):
        qc.h(i)
        qc.rz(0.5, i)
        if i < n_qubits - 1:
            qc.cx(i, i+1)
    return qc
