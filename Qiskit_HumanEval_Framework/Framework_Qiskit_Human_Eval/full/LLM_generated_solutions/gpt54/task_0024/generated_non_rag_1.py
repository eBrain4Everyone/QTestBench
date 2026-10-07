# LLM-generated solution — task_0024
# Generated: 2026-06-23T18:45:10.146118
# Model: gpt54
# Variant: generated_non_rag_1

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from numpy import isclose

def dj_algorithm(oracle: QuantumCircuit) -> bool:
    """ Given a Deutsch-Jozsa oracle in which the final qubit is the "output" qubit, return True if the oracle is constant or False otherwise.
    """
    num_qubits = oracle.num_qubits
    if num_qubits < 2:
        raise ValueError("Oracle must have at least one input qubit and one output qubit.")

    n = num_qubits - 1
    qc = QuantumCircuit(num_qubits, n)

    qc.x(n)
    qc.h(range(num_qubits))
    qc.compose(oracle, inplace=True)
    qc.h(range(n))
    qc.measure(range(n), range(n))

    sampler = StatevectorSampler()
    result = sampler.run([qc], shots=1).result()

    data = result[0].data
    counts = None
    if hasattr(data, "c"):
        counts = data.c.get_counts()
    else:
        for name in dir(data):
            if not name.startswith("_"):
                reg = getattr(data, name)
                if hasattr(reg, "get_counts"):
                    counts = reg.get_counts()
                    break
    if counts is None:
        raise RuntimeError("Unable to extract measurement counts from sampler result.")

    bitstring = next(iter(counts))
    return all(ch == "0" for ch in bitstring)
