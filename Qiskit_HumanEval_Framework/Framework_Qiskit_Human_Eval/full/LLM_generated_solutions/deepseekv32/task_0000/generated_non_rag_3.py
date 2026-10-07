# LLM-generated solution — task_0000
# Generated: 2026-06-23T18:02:06.985636
# Model: deepseekv32
# Variant: generated_non_rag_3

from qiskit import QuantumCircuit
def create_quantum_circuit(n_qubits):
    """ Generate a Quantum Circuit for the given int 'n_qubits' and return it.
    """
    qc = QuantumCircuit(n_qubits)
    for qubit in range(n_qubits):
        qc.h(qubit)
    qc.measure_all()
    return qc
