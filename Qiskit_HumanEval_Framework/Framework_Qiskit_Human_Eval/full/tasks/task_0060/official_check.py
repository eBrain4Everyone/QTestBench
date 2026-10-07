def check(candidate):
    from qiskit.circuit.library import CYGate
    from qiskit.quantum_info.operators import Operator
    result = candidate()
    assert isinstance(result, QuantumCircuit)
    assert result.num_qubits == 2
    assert 'cx' in result.count_ops()
    for gate in result.data:
        op = gate.operation
        assert op.num_qubits == 1 or op.name == 'cx' or op.name == 'barrier'
    assert Operator(result) == Operator(CYGate())
