def check(candidate):
    from qiskit import QuantumCircuit, QuantumRegister
    from qiskit.circuit.gate import Gate
    from qiskit.quantum_info import Operator
    from qiskit.circuit.library import ZGate
    q = QuantumRegister(3, "q")
    circ = QuantumCircuit(q)
    circ.h(q[0])
    circ.cx(q[0], q[1])
    custom_gate = candidate(circ)
    assert type(custom_gate) == Gate
    assert custom_gate.num_qubits == 3
    assert custom_gate.num_clbits == 0

    q = QuantumRegister(1, "q")
    circ = QuantumCircuit(q)
    circ.h(q)
    circ.x(q)
    circ.h(q)
    hxh_gate = candidate(circ)
    hxh_op = Operator(hxh_gate)
    z_op = Operator(ZGate())
    assert hxh_op.equiv(z_op)
