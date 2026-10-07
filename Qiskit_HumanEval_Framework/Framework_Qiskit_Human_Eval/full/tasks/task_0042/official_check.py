def check(candidate):
    result = candidate()
    XX = Operator(Pauli('XX'))
    YY = Operator(Pauli('YY'))
    ZZ = Operator(Pauli('ZZ'))

    op = 0.5 * (XX + YY - 3 * ZZ)
    assert (result == op)
