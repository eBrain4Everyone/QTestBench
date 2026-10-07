def check(candidate):
    from qiskit.circuit.library import RYGate, HGate, CXGate, Measure
    from qiskit.circuit.controlflow import IfElseOp
    from qiskit.circuit import CircuitInstruction

    qc = QuantumCircuit(2,1)
    solution = candidate(qc, 2)
    
    assert len(solution.data) > 0, "Circuit should have operations added"
    
    op = solution.data[0].operation

    assert op.name == "for_loop"
    assert op.num_qubits == 2 and op.num_clbits == 1
    indexset, loop_param, sub_qc = op.params
    assert indexset == range(2)
    
    # Test sub circuit
    data = sub_qc.data
    qr = qc.qregs[0]
    cr = qc.cregs[0]
    assert data[0] == CircuitInstruction(RYGate(pi/2*loop_param), [qr[0]], [])
    assert data[1] == CircuitInstruction(HGate(), [qr[0]], [])
    assert data[2] == CircuitInstruction(CXGate(), [qr[0], qr[1]], [])
    assert data[3] == CircuitInstruction(Measure(), [qr[0]],[cr[0]])
    assert isinstance(data[4].operation, IfElseOp)
    assert set(data[4].qubits) == {qr[0], qr[1]} or set(data[4].qubits) == {qr[1], qr[0]}
    assert [bit._index for bit in data[4].clbits] == [0]
