def check(candidate):
    result = candidate()
    backend = FakeSydneyV2()
    # Optimization level 0 should use trivial qubit mapping
    # i.e. circuit qubit 'i' => device qubit 'i'.
    # This is very unlikely with higher optimization levels
    assert result.layout.initial_index_layout() == list(range(backend.num_qubits))
