# LLM-generated solution — task_0024
# Generated: 2026-06-23T18:45:15.649822
# Model: gpt54
# Variant: generated_non_rag_2

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
    job = sampler.run([qc], shots=1)
    result = job.result()

    data = result[0].data
    counts = None

    if hasattr(data, "c"):
        counts = data.c.get_counts()
    else:
        for attr in dir(data):
            if not attr.startswith("_"):
                reg = getattr(data, attr)
                if hasattr(reg, "get_counts"):
                    counts = reg.get_counts()
                    break

    if counts is None:
        raise RuntimeError("Unable to extract measurement counts from sampler result.")

    bitstring = next(iter(counts))
    return all(ch == "0" for ch in bitstring)
