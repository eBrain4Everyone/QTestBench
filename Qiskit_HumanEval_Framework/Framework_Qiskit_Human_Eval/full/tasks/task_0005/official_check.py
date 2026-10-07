def check(candidate):
    from qiskit.quantum_info import Statevector
    candidate_circuit = candidate()
    assert isinstance(candidate_circuit, QuantumCircuit)
    candidate_sv = Statevector.from_instruction(candidate())
    refrence_sv = Statevector.from_label("1".zfill(candidate_sv.num_qubits))
    assert candidate_sv.equiv(refrence_sv)
