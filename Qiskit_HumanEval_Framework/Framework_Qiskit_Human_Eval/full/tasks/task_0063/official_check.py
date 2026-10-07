def check(candidate):
    from numpy.random import seed
    seed(12345)
    basis = [1, 0, 0, 1, 1]
    circuit = QuantumCircuit(5)
    circuit.x([3, 4])
    circuit.h([0, 3, 4])
    result = candidate(basis, circuit)
    assert result == "1"
