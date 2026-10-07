from statistics import mode
from qiskit.primitives import BitArray
def most_common_result(bits: BitArray) -> str:
    """ Return the most common result as a string of `1`s and `0`s.
    """

    return mode(bits.get_bitstrings())
