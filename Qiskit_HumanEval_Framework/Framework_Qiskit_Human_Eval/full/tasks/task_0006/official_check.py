def check(candidate):
    from qiskit.quantum_info import Statevector

    candidate_circuit = candidate(num_qubits=5)
    assert isinstance(candidate_circuit, QuantumCircuit)
    assert candidate_circuit.num_qubits == 5
    candidate_sv = Statevector.from_instruction(candidate_circuit)
    refrence_sv = Statevector.from_label("1".zfill(candidate_sv.num_qubits))
    assert candidate_sv.equiv(refrence_sv)
