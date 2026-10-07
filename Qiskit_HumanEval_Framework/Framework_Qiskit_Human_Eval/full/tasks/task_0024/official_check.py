def check(candidate):
    balanced = QuantumCircuit(5)
    balanced.cx(3, 4)
    assert candidate(balanced) == False
    constant = QuantumCircuit(9)
    constant.x(8)
    assert candidate(constant) == True
