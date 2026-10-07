# LLM-generated solution — task_0002
# Generated: 2026-06-23T18:03:05.738427
# Model: deepseekv32
# Variant: generated_non_rag_1

from qiskit.quantum_info import Statevector
from math import sqrt
def create_bell_statevector() -> Statevector:
    """ Return a phi+ Bell statevector.
    """
    phi_plus = [sqrt(0.5), 0, 0, sqrt(0.5)]
    return Statevector(phi_plus)
