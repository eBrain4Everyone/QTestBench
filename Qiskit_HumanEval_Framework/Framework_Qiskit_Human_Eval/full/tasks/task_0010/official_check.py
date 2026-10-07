def check(candidate):
    result = candidate()
    XX = Operator([[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]])
    assert XX.equiv(Operator(result))
    for inst in result.data:
        if inst.operation.num_qubits > 1:
            assert inst.operation.name in ["cx", "barrier"]
