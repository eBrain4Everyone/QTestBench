def check(candidate):
    from qiskit import QuantumRegister
    from qiskit.circuit import CircuitInstruction
    from qiskit.circuit.library import HGate
    from qiskit.circuit import Delay
    qr = QuantumRegister(1, name="q")
    data = candidate().data
    assert data[0]==CircuitInstruction(HGate(), [qr[0]], [])
    assert data[1]==CircuitInstruction(Delay(100), [qr[0]], [])
    assert data[2]==CircuitInstruction(HGate(), [qr[0]], [])
