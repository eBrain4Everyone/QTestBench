def check(candidate):
    result = candidate(0,1)
    assert isinstance(result, QuantumCircuit)
    assert result.num_qubits == 2
    assert result.width() == 4
    assert result.depth() == 4
    assert set({'ry': 2, 'measure': 2, 'h': 1, 'cx': 1}.items()).issubset(set(result.count_ops().items()))
