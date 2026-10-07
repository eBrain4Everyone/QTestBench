# LLM-generated solution — task_0003
# Generated: 2026-06-23T18:49:57.140131
# Model: qwen3
# Variant: generated_rag_1

from qiskit import QuantumCircuit
import matplotlib.pyplot as plt

def create_ghz(drawing=False):
    """ Generate a QuantumCircuit for a 3 qubit GHZ State and measure it. If `drawing` is True, return both the circuit object and the Matplotlib drawing of the circuit, otherwise return just the circuit object.
    """
    # Create a 3 qubit quantum circuit with 3 classical bits for measurement
    qc = QuantumCircuit(3, 3)
    
    # Create GHZ state: |000_ + |111_ / sqrt(2)
    # Apply Hadamard to first qubit
    qc.h(0)
    
    # Apply CNOT gates to entangle the qubits
    qc.cx(0, 1)
    qc.cx(1, 2)
    
    # Measure all qubits
    qc.measure([0, 1, 2], [0, 1, 2])
    
    if drawing:
        # Draw the circuit and return both the circuit and the drawing
        # Use the 'mpl' style drawer which returns a matplotlib figure
        circuit_drawer = qc.draw(output='mpl')
        return qc, circuit_drawer
    else:
        return qc
