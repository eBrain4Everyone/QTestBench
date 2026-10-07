# LLM-generated solution — task_0003
# Generated: 2026-06-23T18:49:52.395127
# Model: qwen3
# Variant: generated_non_rag_3

from qiskit import QuantumCircuit
import matplotlib.pyplot as plt

def create_ghz(drawing=False):
    """ Generate a QuantumCircuit for a 3 qubit GHZ State and measure it. If `drawing` is True, return both the circuit object and the Matplotlib drawing of the circuit, otherwise return just the circuit object.
    """
    # Create a quantum circuit with 3 qubits and 3 classical bits
    qc = QuantumCircuit(3, 3)
    
    # Create GHZ state: (|000_ + |111_)/_2
    qc.h(0)           # Apply Hadamard to first qubit
    qc.cx(0, 1)       # Apply CNOT with qubit 0 as control, qubit 1 as target
    qc.cx(0, 2)       # Apply CNOT with qubit 0 as control, qubit 2 as target
    
    # Measure all qubits
    qc.measure([0, 1, 2], [0, 1, 2])
    
    if drawing:
        # Draw the circuit and return both circuit and drawing
        circuit_image = qc.draw('mpl')
        return qc, circuit_image
    else:
        return qc
