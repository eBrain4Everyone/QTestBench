def check(candidate):
    n = 5
    qc_inv = candidate(n)

    expected_qc = QuantumCircuit(n)
    for i in range(2):
        expected_qc.h(i+1)

    for i in range(2):
        expected_qc.cx(i+1, i+2+1)
    
    expected_qc_inv = expected_qc.inverse()

    assert isinstance(qc_inv, QuantumCircuit)
    assert qc_inv == expected_qc_inv
