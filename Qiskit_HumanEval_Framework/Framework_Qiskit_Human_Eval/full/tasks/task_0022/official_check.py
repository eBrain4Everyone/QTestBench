def check(candidate):
    result = candidate()
    backend = FakeAuckland()
    assert result.num_qubits == backend.num_qubits
