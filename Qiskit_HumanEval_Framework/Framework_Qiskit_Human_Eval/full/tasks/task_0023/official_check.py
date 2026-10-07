def check(candidate):
    from qiskit.quantum_info import Operator

    qc = QuantumCircuit(3)
    constant_0_oracle = Operator(qc)
    qc.x(2)
    constant_1_oracle = Operator(qc)
    result = Operator(candidate())
    assert result.equiv(constant_0_oracle) or result.equiv(constant_1_oracle)
