def check(candidate):
    from qiskit.circuit.library import SwapGate
    from qiskit.quantum_info.operators import Operator
    result = candidate()
    assert isinstance(result, QuantumCircuit)
    assert result.num_qubits == 2
    assert dict(result.count_ops()) == {'cx': 3}
    assert Operator(result) == Operator(SwapGate())
