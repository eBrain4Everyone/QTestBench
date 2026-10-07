def check(candidate):
    import numpy as np
    from qiskit.circuit.library import efficient_su2
    from qiskit.quantum_info import Operator
    circ = efficient_su2(3).decompose()
    circ = circ.assign_parameters(np.random.random(circ.num_parameters))
    circ_can = candidate(circ)
    op_or = Operator(circ)
    op_can = Operator(circ_can)
    assert Operator.equiv(op_or, op_can, rtol=0.1, atol=0.1), "Operators are not the same"
    assert isinstance(circ_can, QuantumCircuit), "Not a quantum circuit"
    for instruction in circ_can.data:
        instr, qargs, cargs = instruction.operation, instruction.qubits, instruction.clbits
        if instr.num_qubits == 1 and instr.name not in {"h", "tdg", "t"}:
            raise AssertionError("Circuit contains gates outside the given dense subset")
