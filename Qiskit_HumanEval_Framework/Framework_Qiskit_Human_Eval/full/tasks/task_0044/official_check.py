def check(candidate):
    from qiskit.quantum_info import Statevector
    result = candidate()
    top = QuantumCircuit(1)
    top.x(0);
    bottom = QuantumCircuit(2)
    bottom.cry(0.2, 0, 1)
    tensored = bottom.tensor(top)
    assert Statevector.from_instruction(result).equiv(Statevector.from_instruction(tensored))
