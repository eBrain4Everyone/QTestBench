def check(candidate):
    from collections import OrderedDict
    from qiskit.transpiler.passes import UnitarySynthesis
    from qiskit.transpiler import PassManager
    gr_state_circ_can = candidate()
    assert isinstance(gr_state_circ_can, QuantumCircuit)
    gr_state_circ_exp_ops = OrderedDict([("cz", 144), ("h", 127)])
    basis_gates = ["cz", "h"]
    pm = PassManager([UnitarySynthesis(basis_gates)])
    gr_state_circ_can_ops = pm.run(gr_state_circ_can.decompose()).count_ops()
    assert gr_state_circ_can_ops == gr_state_circ_exp_ops
