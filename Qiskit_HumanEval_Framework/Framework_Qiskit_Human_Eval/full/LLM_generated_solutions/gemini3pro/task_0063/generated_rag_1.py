# LLM-generated solution — task_0063
# Generated: 2026-06-23T18:42:00.485230
# Model: gemini3pro
# Variant: generated_rag_1

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
from numpy.random import randint

def bb84_circuit_generate_key(senders_basis: [int], circuit: QuantumCircuit) -> str:
    circuit = circuit.copy()
    num_qubits = len(senders_basis)
    
    if num_qubits == 0:
        return ""
        
    receivers_basis = randint(0, 2, num_qubits)
    
    for i in range(num_qubits):
        if receivers_basis[i] == 1:
            circuit.h(i)
            
    circuit.measure_all()
    
    simulator = AerSimulator()
    result = simulator.run(circuit, shots=1).result()
    counts = result.get_counts()
    
    measured_string = list(counts.keys())[0].split()[0]
    measured_bits = measured_string[::-1]
    
    key = ""
    for i in range(num_qubits):
        if senders_basis[i] == receivers_basis[i]:
            key += measured_bits[i]
            
    return key
