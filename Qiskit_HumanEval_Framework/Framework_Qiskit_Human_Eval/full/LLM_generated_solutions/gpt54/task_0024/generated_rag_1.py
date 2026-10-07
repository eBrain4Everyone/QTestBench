# LLM-generated solution — task_0024
# Generated: 2026-06-23T18:45:25.666862
# Model: gpt54
# Variant: generated_rag_1

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from numpy import isclose

def dj_algorithm(oracle: QuantumCircuit) -> bool:
    """ Given a Deutsch-Jozsa oracle in which the final qubit is the "output" qubit, return True if the oracle is constant or False otherwise.
    """
    n_qubits = oracle.num_qubits
    if n_qubits < 2:
        raise ValueError("Oracle must have at least one input qubit and one output qubit.")

    n_input = n_qubits - 1

    qc = QuantumCircuit(n_qubits, n_input)

    qc.x(n_input)
    qc.h(range(n_qubits))
    qc.compose(oracle, inplace=True)
    qc.h(range(n_input))
    qc.measure(range(n_input), range(n_input))

    sampler = StatevectorSampler()
    result = sampler.run([qc], shots=1024).result()

    pub_result = result[0]
    data_bin = pub_result.data.c
    counts = data_bin.get_counts()

    zero_key = "0" * n_input
    zero_counts = counts.get(zero_key, 0)
    total_counts = sum(counts.values())

    return isclose(zero_counts / total_counts, 1.0)
