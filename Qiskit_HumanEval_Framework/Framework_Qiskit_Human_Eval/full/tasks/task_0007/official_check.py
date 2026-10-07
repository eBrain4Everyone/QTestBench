def check(candidate):
    circuit = candidate()
    assert circuit.num_qubits == 1
    assert circuit.data[0].operation.name == "rx"
    assert circuit.data[0].operation.params[0].name == "theta"
