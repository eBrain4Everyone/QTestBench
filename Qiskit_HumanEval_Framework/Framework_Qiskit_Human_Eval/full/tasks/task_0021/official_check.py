def check(candidate):
    result = candidate()
    backend = FakeOslo()
    assert result.num_qubits == backend.num_qubits
