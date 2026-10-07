def check(candidate):
    diag = [1, 1j, -1, -1j]
    qc = candidate(diag)
    assert isinstance(qc, QuantumCircuit), "The function should return a QuantumCircuit"
    
    op_circuit = Operator(qc)
    
    expected_diagonal = Diagonal(diag)
    op_expected = Operator(expected_diagonal)
    
    assert op_circuit.equiv(op_expected), "The circuit does not match the expected Diagonal gate"
