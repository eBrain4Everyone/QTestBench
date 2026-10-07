def check(candidate):
    from qiskit.quantum_info import Statevector
    from qiskit.transpiler.passes import CheckMap
    from qiskit.converters import circuit_to_dag
    coupling = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6]]
    coupling_map = CouplingMap(couplinglist=coupling)
    result = candidate(coupling)
    chkmp = CheckMap(coupling_map)
    chkmp.run(circuit_to_dag(result))
    assert chkmp.property_set["is_swap_mapped"] == True
    solution = QuantumCircuit(7)
    solution.h(0)
    solution.cx(0, range(1, 7))
    ls = LookaheadSwap(coupling_map=coupling_map)
    pass_manager = PassManager(ls)
    lookahead_circ = pass_manager.run(solution)
    assert Statevector.from_instruction(lookahead_circ).equiv(Statevector.from_instruction(result))
