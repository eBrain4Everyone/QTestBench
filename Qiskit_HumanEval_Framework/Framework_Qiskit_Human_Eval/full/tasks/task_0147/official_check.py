from qiskit.quantum_info import Operator

def check(candidate):
    expected = QuantumCircuit(6)
    expected.h([0, 4, 5])
    mcy_gate = YGate().control(num_ctrl_qubits=4)
    expected.append(mcy_gate, range(5))

    solution = QuantumCircuit(6)
    solution.h([0, 4, 5])
    solution = candidate(solution)
    assert Operator(solution) == Operator(expected)
