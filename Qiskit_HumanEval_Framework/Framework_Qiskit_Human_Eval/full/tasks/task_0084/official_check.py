def check(candidate):
    qc = candidate()
    assert isinstance(qc, QuantumCircuit)
    assert qc.num_qubits == 2
    assert any(instr.operation.name.startswith('cu3') or 'u3' in instr.operation.name for instr in qc.data)
