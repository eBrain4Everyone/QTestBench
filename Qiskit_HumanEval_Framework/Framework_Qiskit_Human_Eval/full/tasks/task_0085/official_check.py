def check(candidate):
    from qiskit.quantum_info import Statevector
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0,1)
    qasm_str = candidate(qc)
    circuit = QuantumCircuit.from_qasm_str(qasm_str)
    assert Statevector.from_instruction(circuit) == Statevector.from_instruction(qc)
