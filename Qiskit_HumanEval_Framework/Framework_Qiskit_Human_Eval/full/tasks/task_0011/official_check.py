def check(candidate):
    test_circuit = QuantumCircuit(2)
    test_circuit.u(0.39702, 0.238798, 0.298374, 0)
    test_circuit.cx(0, 1)

    result = candidate(test_circuit)
    assert isinstance(result, Statevector)
    assert Statevector.from_instruction(test_circuit).equiv(result)
