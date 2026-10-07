def check(candidate):
    result = candidate()
    assert type(result) == DAGCircuit
    assert result.num_qubits() == 3
    assert result.depth() == 3
    assert dict(result.count_ops()) == {'h': 1, 'cx': 1, 'measure':1}
