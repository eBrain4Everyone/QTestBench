# LLM-generated solution — task_0063
# Generated: 2026-06-23T18:41:21.177503
# Model: gemini3pro
# Variant: generated_non_rag_3

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
from numpy.random import randint

def bb84_circuit_generate_key(senders_basis: [int], circuit: QuantumCircuit) -> str:
    n = min(circuit.num_qubits, len(senders_basis))
    qc = circuit.copy()
    
    receivers_basis = randint(2, size=circuit.num_qubits)
    
    for i in range(circuit.num_qubits):
        if receivers_basis[i] == 1:
            qc.h(i)
            
    qc.measure_all()
    
    simulator = AerSimulator()
    result = simulator.run(qc, shots=1).result()
    counts = result.get_counts()
    
    measured_str = list(counts.keys())[0].split()[0]
    measured_bits = measured_str[::-1]
    
    key = ""
    for i in range(n):
        if senders_basis[i] == receivers_basis[i]:
            key += measured_bits[i]
            
    return key
