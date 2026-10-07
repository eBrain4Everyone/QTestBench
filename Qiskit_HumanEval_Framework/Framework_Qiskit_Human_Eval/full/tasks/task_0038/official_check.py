def check(candidate):
    from qiskit import QuantumRegister
    from qiskit.circuit import CircuitInstruction
    from math import pi
    from qiskit.circuit.library import HGate, CRZGate, CRYGate
    qr = QuantumRegister(2, name="q")
    theta = pi/2
    data = candidate(theta).data
    assert data[0]==CircuitInstruction(HGate(), [qr[0]], [])
    assert data[1]==CircuitInstruction(CRZGate(theta), [qr[0], qr[1]], [])
    assert data[2]==CircuitInstruction(HGate(), [qr[1]], [])
    assert data[3]==CircuitInstruction(CRYGate(theta), [qr[1], qr[0]], [])
