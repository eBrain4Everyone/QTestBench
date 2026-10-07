def check(candidate):
    qc = candidate()
    assert isinstance(qc, QuantumCircuit)
    
    c3sx_instructions = [inst for inst in qc.data if isinstance(inst.operation, C3SXGate)]
    assert len(c3sx_instructions) == 1
    
    assert c3sx_instructions[0].qubits == tuple([qc.qubits[i] for i in range(4)])
