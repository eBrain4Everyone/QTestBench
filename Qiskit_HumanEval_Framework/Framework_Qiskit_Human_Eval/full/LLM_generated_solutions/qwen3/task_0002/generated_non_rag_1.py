# LLM-generated solution — task_0002
# Generated: 2026-06-23T18:48:56.277030
# Model: qwen3
# Variant: generated_non_rag_1

from qiskit.quantum_info import Statevector
from math import sqrt

def create_bell_statevector() -> Statevector:
    """ Return a phi+ Bell statevector.
    """
    # The phi+ Bell state is (|00_ + |11_) / sqrt(2)
    # In computational basis ordering [00, 01, 10, 11], this corresponds to
    # coefficients [1/sqrt(2), 0, 0, 1/sqrt(2)]
    return Statevector([1/sqrt(2), 0, 0, 1/sqrt(2)])
