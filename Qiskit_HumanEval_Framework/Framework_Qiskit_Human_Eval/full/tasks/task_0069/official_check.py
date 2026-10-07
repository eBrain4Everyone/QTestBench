def check(candidate):
    result = candidate()
    assert isinstance(result, QuantumCircuit)
    assert result.num_qubits == 2
    assert result.depth() == 4
    assert dict(result.count_ops()) == {'h': 2, 'cs': 1, 'csdg': 1}
