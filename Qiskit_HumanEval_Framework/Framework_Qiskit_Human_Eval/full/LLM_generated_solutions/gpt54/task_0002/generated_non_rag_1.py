# LLM-generated solution — task_0002
# Generated: 2026-06-23T18:43:19.010634
# Model: gpt54
# Variant: generated_non_rag_1

from qiskit.quantum_info import Statevector
from math import sqrt

def create_bell_statevector() -> Statevector:
    """ Return a phi+ Bell statevector.
    """
    return Statevector([1 / sqrt(2), 0, 0, 1 / sqrt(2)])
