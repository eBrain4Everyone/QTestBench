def check(candidate):
    from qiskit.circuit.library import RXGate, RZGate
    circ = QuantumCircuit(2)
    theta = Parameter("θ")
    circ.rx(0.1, 1)
    circ.ry(theta, 1)
    circ.rx(theta, 0)
    circ.cp(theta, 0, 1)
    circ.rz(0.4, 0)
    circ_can = candidate(circ)
    assert isinstance(circ_can, QuantumCircuit), "Not a quantum circuit"
    assert len(circ_can.parameters) == 0, "Circuit consists of gates with unassigned parameters."
    has_rx = False
    has_rz = False
    for instruction in circ_can:
        instr, qargs, cargs = instruction.operation, instruction.qubits, instruction.clbits
        if isinstance(instr, RXGate):
            has_rx = True
        if isinstance(instr, RZGate):
            has_rz = True
    assert has_rx is True, "Removed rx gates with assigned parameters from the circuit"
    assert has_rz is True, "Removed rz gates with assigned parameters from the circuit"
