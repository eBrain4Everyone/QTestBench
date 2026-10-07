from qiskit.quantum_info.operators import Operator, Pauli
def combine_op() -> Operator:
    """ Combine the following three operators XX YY ZZ as: 0.5 * (XX + YY - 3 * ZZ).
    """

    XX = Operator(Pauli('XX'))
    YY = Operator(Pauli('YY'))
    ZZ = Operator(Pauli('ZZ'))

    op = 0.5 * (XX + YY - 3 * ZZ)
    return op
