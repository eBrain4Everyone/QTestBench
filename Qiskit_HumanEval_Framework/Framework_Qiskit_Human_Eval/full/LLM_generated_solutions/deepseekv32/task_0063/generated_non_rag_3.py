# LLM-generated solution — task_0063
# Generated: 2026-06-23T18:11:44.058734
# Model: deepseekv32
# Variant: generated_non_rag_3

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
from numpy.random import randint

def bb84_circuit_generate_key(senders_basis: [int], circuit: QuantumCircuit) -> str:
    backend = AerSimulator()
    result = backend.run(circuit, shots=1, memory=True).result()
    measurement = result.get_memory()[0]
    key = ""
    for i in range(len(senders_basis)):
        if senders_basis[i] == 0:
            key += measurement[i]
        else:
            if measurement[i] == "0":
                key += "1"
            else:
                key += "0"
    return key
