# LLM-generated solution — task_0024
# Generated: 2026-06-23T18:45:20.037873
# Model: gpt54
# Variant: generated_non_rag_3

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from numpy import isclose

def dj_algorithm(oracle: QuantumCircuit) -> bool:
    """ Given a Deutsch-Jozsa oracle in which the final qubit is the "output" qubit, return True if the oracle is constant or False otherwise.
    """
    num_qubits = oracle.num_qubits
    if num_qubits < 2:
        raise ValueError("Oracle must have at least one input qubit and one output qubit.")

    n_inputs = num_qubits - 1

    qc = QuantumCircuit(num_qubits, n_inputs)
    qc.x(num_qubits - 1)
    qc.h(range(num_qubits))
    qc.compose(oracle, inplace=True)
    qc.h(range(n_inputs))
    qc.measure(range(n_inputs), range(n_inputs))

    sampler = StatevectorSampler()
    job = sampler.run([qc], shots=1)
    result = job.result()

    data = result[0].data
    counts = data.c.get_counts()
    bitstring = next(iter(counts))

    return bitstring == "0" * n_inputs
