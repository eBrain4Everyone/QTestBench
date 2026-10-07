def check(candidate):
    result = candidate(3,3)
    assert result.num_qubits == 3
    assert isinstance(result, LinearFunction)
