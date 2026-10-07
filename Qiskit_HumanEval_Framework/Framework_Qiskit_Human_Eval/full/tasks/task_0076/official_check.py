def check(candidate):
    from qiskit.transpiler import PassManager
    from qiskit import QuantumCircuit
    hxh_pass = candidate()
    # Be lenient and accept both class and instance of class
    if not isinstance(hxh_pass, TransformationPass):
        hxh_pass = hxh_pass()
    assert isinstance(hxh_pass, TransformationPass)
    passmanager = PassManager(hxh_pass)
    qc = QuantumCircuit(1)
    qc.x(0)
    qc.z(0)
    result = passmanager.run(qc)
    result_op_strings = list(
        map(lambda circuit_inst: circuit_inst.operation.name, result.data)
    )
    assert result_op_strings == ["x", "h", "x", "h"]
    qc = QuantumCircuit(3)
    qc.h(1)
    qc.z(1)
    qc.cz(0, 1)
    qc.cx(1, 2)
    result = passmanager.run(qc)
    result_op_strings = list(
        map(lambda circuit_inst: circuit_inst.operation.name, result.data)
    )
    assert result_op_strings == ["h", "h", "x", "h", "cz", "cx"]
