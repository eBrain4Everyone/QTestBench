def check(candidate):
    from qiskit.quantum_info import Clifford
    qc_comp = random_clifford(5).to_circuit()
    op_comp = Operator(qc_comp)
    can_circ_list = candidate(qc_comp, 10)
    for item in can_circ_list:
        assert Operator(item).equiv(op_comp, rtol = 0.4, atol = 0.4)
        try:
            Clifford(item)
        except Exception as err:
            raise AssertionError("The circuit is not a Clifford circuit.") from err
