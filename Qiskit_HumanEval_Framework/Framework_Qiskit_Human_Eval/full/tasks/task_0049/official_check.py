def check(candidate):
    from qiskit.quantum_info import Statevector
    result = candidate()
    assert isinstance(result, QuantumCircuit)
    assert result.num_qubits == 2
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0,1)
    circuit.h(0)
    assert Statevector.from_instruction(result).equiv(Statevector.from_instruction(circuit))
