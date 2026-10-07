def check(candidate):
    backend = FakeCairoV2()
    circuit = QuantumCircuit(4, 3)
    circuit.cx([0, 1, 2, 3], [1, 2, 3, 0])
    t_circuit = candidate(circuit)
    assert t_circuit.num_qubits == backend.num_qubits
    for inst in t_circuit.data:
        assert inst.operation.name in backend.configuration().basis_gates
