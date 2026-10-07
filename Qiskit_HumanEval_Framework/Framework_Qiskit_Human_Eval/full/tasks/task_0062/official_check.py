def check(candidate):
    from qiskit.quantum_info import Statevector
    from numpy.random import randint, seed
    seed(12345)
    qubits = 5
    state = randint(2, size=qubits)
    basis = randint(2, size=qubits)
    result = candidate(state, basis)
    assert isinstance(result, QuantumCircuit)
    assert result.num_qubits == qubits
    assert result.count_ops()['h'] == sum(basis)
    assert result.count_ops()['x'] == sum(state)
    solution = QuantumCircuit(5)
    solution.x([1,2,3])
    solution.h([0,3])
    assert Statevector.from_instruction(result).equiv(Statevector.from_instruction(solution))
