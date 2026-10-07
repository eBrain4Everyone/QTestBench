def check(candidate):
    from qiskit.circuit.library import QFT as QiskitQFT
    from qiskit.quantum_info.operators import Operator
    result = candidate(3)
    assert isinstance(result, QuantumCircuit)
    assert result.num_qubits == 3
    for gate in result.data:
        op = gate.operation
        assert op.num_qubits <= 2 or op.name == 'barrier'
    solution = QiskitQFT(3)
    assert Operator(result).equiv(Operator(solution))
