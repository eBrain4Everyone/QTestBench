def check(candidate):
    from qiskit.quantum_info import Operator
    for num_qubits in [1, 3, 8]:
        qft = QFT(num_qubits=num_qubits, do_swaps=False, inverse=True)
        response = candidate(num_qubits)
        assert Operator(qft) == Operator(response)
