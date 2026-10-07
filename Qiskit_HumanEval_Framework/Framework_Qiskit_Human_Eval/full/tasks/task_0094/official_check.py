def check(candidate):
    from qiskit.quantum_info import Operator
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0,1)
    qasm_str = candidate(qc)
    circuit = qiskit.qasm3.loads(qasm_str)
    assert Operator(circuit).equiv(Operator(qc)), "Loaded QASM does not match circuit"
