def check(candidate):
    from qiskit.circuit.library import CHGate
    from qiskit.quantum_info.operators import Operator
    result = candidate()
    assert isinstance(result, QuantumCircuit)
    assert result.num_qubits == 2
    assert dict(result.count_ops()) == {'ry': 2, 'cx': 1}
    assert Operator(result) == Operator(CHGate())
