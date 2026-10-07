def check(candidate):
    from qiskit.quantum_info import Operator
    circuit = QuantumCircuit(1)
    circuit.h(0)
    circuit.barrier()
    circuit.x(0)
    candidate_circuit = candidate(circuit)
    for inst in candidate_circuit.data:
        assert inst.operation.name != 'barrier'
    assert Operator(circuit).equiv(candidate_circuit)
