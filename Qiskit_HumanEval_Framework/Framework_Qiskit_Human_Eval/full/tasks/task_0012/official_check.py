def check(candidate):
    result = candidate()
    solution = QuantumCircuit(2)
    solution.h(0)
    solution.cx(0, 1)
    assert Operator(solution).equiv(result)
