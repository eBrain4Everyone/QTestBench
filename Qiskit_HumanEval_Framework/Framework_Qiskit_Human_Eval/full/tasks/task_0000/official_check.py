def check(candidate):
    result = candidate(3)
    assert isinstance(result, QuantumCircuit)
    assert result.num_qubits == 3
