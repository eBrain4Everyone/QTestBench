def check(candidate):
    instruction = candidate()
    assert instruction.name == "bell_instruction"
    assert instruction.num_qubits == 2
    circ = QuantumCircuit(2, 2)
    circ.h(0)
    circ.cx(0,1)
    circ.measure([0, 1], [0, 1])
    assert instruction.definition == circ
