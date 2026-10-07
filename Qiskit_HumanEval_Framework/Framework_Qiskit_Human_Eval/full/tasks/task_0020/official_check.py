def check(candidate):
    result = candidate()
    result.remove_final_measurements()
    backend = FakePerth()
    assert result.num_qubits == backend.num_qubits
    assert result.layout.initial_index_layout()[:3] == [2, 4, 6]
