def check(candidate):
    from qiskit.circuit import QuantumCircuit
    result = candidate()
    solution = efficient_su2(num_qubits=3, reps=1, insert_barriers=True)
    assert isinstance(result, QuantumCircuit)
    assert solution.num_qubits == result.num_qubits
    barrier_ops = [op for op in result if op.operation.name == 'barrier']
    assert len(barrier_ops) > 0, 'Circuit should contain barriers when insert_barriers=True'
    # Check reps by comparing the number of parameters
    assert result.num_parameters == solution.num_parameters
