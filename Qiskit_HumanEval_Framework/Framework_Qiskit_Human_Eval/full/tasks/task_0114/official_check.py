def check(candidate):
    cmap = candidate()
    edges = set(cmap.get_edges())
    assert edges == { (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5,6) }
    assert len(cmap.physical_qubits) == 8
