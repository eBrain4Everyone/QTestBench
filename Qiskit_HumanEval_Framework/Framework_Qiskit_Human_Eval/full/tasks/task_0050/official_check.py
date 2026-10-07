def check(candidate):
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.h(1)
    qc.h(0)
    expected_qc = QuantumCircuit(2)
    expected_qc.cx(0, 1)
    expected_qc.h(1)
    expected_qc.h(0)
    assert candidate(qc, 0)==expected_qc
