def check(candidate):
    from qiskit.quantum_info import Clifford
    result = candidate(3)
    assert result.num_qubits == 3
    assert isinstance(result, Clifford)
