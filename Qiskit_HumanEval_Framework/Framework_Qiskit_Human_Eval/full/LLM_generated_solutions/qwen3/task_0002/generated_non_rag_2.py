# LLM-generated solution — task_0002
# Generated: 2026-06-23T18:49:00.191961
# Model: qwen3
# Variant: generated_non_rag_2

from qiskit.quantum_info import Statevector
from math import sqrt

def create_bell_statevector() -> Statevector:
    """ Return a phi+ Bell statevector.
    """
    # The |_+_ Bell state is (|00_ + |11_)/_2
    # In Qiskit's computational basis ordering, this corresponds to the statevector:
    # [1/_2, 0, 0, 1/_2]
    return Statevector([1/sqrt(2), 0, 0, 1/sqrt(2)])
