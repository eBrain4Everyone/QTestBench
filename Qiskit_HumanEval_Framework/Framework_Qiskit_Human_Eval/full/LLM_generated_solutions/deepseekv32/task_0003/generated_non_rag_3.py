# LLM-generated solution — task_0003
# Generated: 2026-06-23T18:05:38.352024
# Model: deepseekv32
# Variant: generated_non_rag_3

from qiskit import QuantumCircuit
def create_ghz(drawing=False):
    """ Generate a QuantumCircuit for a 3 qubit GHZ State and measure it. If `drawing` is True, return both the circuit object and the Matplotlib drawing of the circuit, otherwise return just the circuit object.
    """
    qc = QuantumCircuit(3, 3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(0, 2)
    qc.measure([0, 1, 2], [0, 1, 2])
    if drawing:
        drawing_obj = qc.draw(output='mpl')
        return qc, drawing_obj
    else:
        return qc
