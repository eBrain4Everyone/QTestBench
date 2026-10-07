def check(candidate):
    from qiskit.quantum_info import Operator
    qc1 = QuantumCircuit(2)
    qc1.x(0)
    qc1.h(1)
    custom = qc1.to_gate().control(2)
    qc2 = QuantumCircuit(4)
    qc2.append(custom, [0, 3, 1, 2])
    candidate_circuit = candidate()
    assert Operator(qc2).equiv(candidate_circuit)
