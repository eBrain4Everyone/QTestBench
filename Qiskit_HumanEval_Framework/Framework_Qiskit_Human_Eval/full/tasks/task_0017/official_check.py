def check(candidate):
    from qiskit.quantum_info import Operator
    trial_circuit = QuantumCircuit(2)
    trial_circuit.h(0)
    trial_circuit.u(0.3, 0.1, 0.1, 1)
    trial_circuit.cp(np.pi / 4, 0, 1)
    trial_circuit.h(0)
    output = candidate(trial_circuit)
    assert Operator(output).equiv(Operator(trial_circuit))
    for inst in output.data:
        assert inst.operation.name in ["cx", "id", "rz", "sx", "x", "u"]
