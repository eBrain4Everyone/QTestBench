def check(candidate):
    result = candidate()
    op = Operator(np.eye(2 ** 3))
    YX = Operator(Pauli('YX'))
    expected = op.compose(YX, qargs=[0, 2], front=True)
    assert(result == expected)
