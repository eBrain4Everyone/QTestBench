# LLM-generated solution — task_0063
# Generated: 2026-06-23T18:12:09.222083
# Model: deepseekv32
# Variant: generated_rag_1

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
from numpy.random import randint

def bb84_circuit_generate_key(senders_basis: [int], circuit: QuantumCircuit) -> str:
    backend = AerSimulator()
    result = backend.run(circuit, shots=1).result()
    statevector = result.get_statevector()
    
    key_bits = []
    for i in range(len(senders_basis)):
        if senders_basis[i] == 0:
            if abs(statevector[2*i])**2 > 0.9:
                key_bits.append('0')
            elif abs(statevector[2*i+1])**2 > 0.9:
                key_bits.append('1')
            else:
                key_bits.append('_')
        else:
            if abs(statevector[2*i] + statevector[2*i+1])**2/2 > 0.9:
                key_bits.append('0')
            elif abs(statevector[2*i] - statevector[2*i+1])**2/2 > 0.9:
                key_bits.append('1')
            else:
                key_bits.append('_')
    
    return ''.join(key_bits)
