def check(candidate):
    result = candidate()
    assert isinstance(result, QuantumCircuit)
    assert result.num_qubits == 2
    assert result.depth() == 3
    assert dict(result.count_ops()) == {"h": 2, "csx": 1}
