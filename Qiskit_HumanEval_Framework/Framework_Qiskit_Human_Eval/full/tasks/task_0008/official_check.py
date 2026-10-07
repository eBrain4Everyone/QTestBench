def check(candidate):
    from qiskit.quantum_info import Operator
    import math

    circuit = candidate()
    assert circuit.num_qubits == 1
    assert circuit.data[0].operation.name == "rx"
    assert circuit.data[0].operation.params[0].name == "theta"

    candidate_circuit = candidate(value=math.pi * 3 / 4)
    solution_circuit = QuantumCircuit(1)
    solution_circuit.rx((math.pi * 3 / 4), 0)
    assert Operator(solution_circuit).equiv(Operator(candidate_circuit))
