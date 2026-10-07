def check(candidate):
    from qiskit.quantum_info import Operator
    n_qubits = 6
    synthesized_qc = candidate(n_qubits)
    qc = random_clifford(n_qubits, seed=1234)
    expected = synth_clifford_full(qc)
    assert Operator(synthesized_qc) == Operator(expected)
