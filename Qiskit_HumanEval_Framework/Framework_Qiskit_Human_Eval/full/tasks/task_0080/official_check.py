def check(candidate):
    qc = QuantumCircuit(4)
    qc.reset(0)
    qc.tdg(0)
    assert candidate(qc) == 1

    qc.cx(0, [1, 2])
    assert candidate(qc) == 3

    qc.measure_all()
    assert candidate(qc) == 3
