# LLM-generated solution — task_0002
# Generated: 2026-06-23T18:03:17.707216
# Model: deepseekv32
# Variant: generated_non_rag_2

from qiskit.quantum_info import Statevector
from math import sqrt
def create_bell_statevector() -> Statevector:
    """ Return a phi+ Bell statevector.
    """
    zero = Statevector.from_label('00')
    h_gate = [[1/sqrt(2), 1/sqrt(2)], [1/sqrt(2), -1/sqrt(2)]]
    cx_gate = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]
    zero = zero.evolve(h_gate, [0])
    zero = zero.evolve(cx_gate, [0, 1])
    return zero
