def check(candidate):
    from qiskit.quantum_info import Operator

    result = candidate()
    assert isinstance(result, QuantumCircuit)
    solution = QuantumCircuit(1)
    solution.u(np.pi / 2, np.pi / 2, np.pi / 2, 0)
    assert Operator(solution).equiv(Operator(result))
