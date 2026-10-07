def check(candidate):
    from qiskit.quantum_info.operators import Operator
    s = "1111"
    result = candidate(s)
    assert isinstance(result, QuantumCircuit)
    assert result.num_qubits == 5
    solution = QuantumCircuit(5)
    for i in range(4):
        solution.cx(i, 4)
    assert Operator(result).equiv(Operator(solution))
