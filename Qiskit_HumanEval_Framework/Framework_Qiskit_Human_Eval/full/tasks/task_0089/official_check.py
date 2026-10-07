def check(candidate):
    from qiskit.quantum_info import Operator
    solution_register = QuantumRegister(3)
    solution_circuit = QuantumCircuit(solution_register)
    c3h_gate = HGate().control(2)
    solution_circuit.append(c3h_gate, solution_register)
    qc = candidate()
    assert Operator(qc).equiv(solution_circuit)
