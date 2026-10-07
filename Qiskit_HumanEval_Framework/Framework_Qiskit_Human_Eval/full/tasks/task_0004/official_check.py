def check(candidate):
    from qiskit.quantum_info import Operator
    matrix = [[0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]]
    solution = QuantumCircuit(2)
    solution.unitary(matrix, [0, 1])
    assert Operator(solution).equiv(Operator(candidate()))
