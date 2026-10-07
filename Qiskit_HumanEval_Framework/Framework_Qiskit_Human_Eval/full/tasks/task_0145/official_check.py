def check(candidate):
    from qiskit.circuit.library import QFT
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Operator

    # Test multiple values of n
    for n in [1, 2, 3, 5, 8, 10]:
        candidate_circ = candidate(n)

        # Ensure the result is a QuantumCircuit
        assert isinstance(candidate_circ, QuantumCircuit), "Returned object is not a QuantumCircuit"

        # Ensure the circuit has the correct number of qubits
        assert candidate_circ.num_qubits == n, f"Expected {n} qubits, but got {candidate_circ.num_qubits}"

        # Verify that the returned circuit is equivalent to the expected inverse QFT circuit
        candidate_op = Operator(candidate_circ)
        test_circ = QFT(n, approximation_degree=0, inverse=True)
        test_op = Operator(test_circ)

        assert test_op.equiv(candidate_op), "The circuit doesn't match the expected inverse QFT circuit"

    # Edge case: n=0 (should raise an error or return an empty circuit)
    try:
        candidate_circ = candidate(0)
        assert candidate_circ.num_qubits == 0, "For n=0, circuit should have 0 qubits"
    except Exception:
        pass  # Allow exception if function correctly handles invalid input
