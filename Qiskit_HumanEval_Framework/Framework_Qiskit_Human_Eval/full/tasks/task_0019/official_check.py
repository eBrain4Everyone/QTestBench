def check(candidate):
    result = candidate()
    result.remove_final_measurements()
    backend = FakeTorontoV2()
    # Check initial layout is not the trivial layout (this is very unlikely
    # if transpiled with optimization level 3)
    assert result.layout.initial_index_layout() != list(range(backend.num_qubits))
    # Optimization level 3 should easily find circuits with depth < 200
    assert result.depth() < 150
