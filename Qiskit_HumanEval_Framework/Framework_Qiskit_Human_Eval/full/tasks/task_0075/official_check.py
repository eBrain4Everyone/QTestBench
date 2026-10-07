def check(candidate):
    # 101
    qc = QuantumCircuit(3)
    qc.x([0, 2])
    qc.measure_all()
    assert candidate(qc) == [True, False, True]

    # 00011
    qc = QuantumCircuit(5)
    qc.x([3, 4])
    qc.measure_all()
    assert candidate(qc) == [False] * 3 + [True] * 2

    # 111011111
    qc = QuantumCircuit(9)
    qc.x(range(9))
    qc.x(3)
    qc.measure_all()
    assert candidate(qc) == [True] * 3 + [False] + [True] * 5
