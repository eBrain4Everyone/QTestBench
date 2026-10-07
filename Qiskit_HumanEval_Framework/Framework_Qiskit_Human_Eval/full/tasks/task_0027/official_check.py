def check(candidate):
    from qiskit.quantum_info import Statevector
    from qiskit.converters import dag_to_circuit
    result = candidate()
    assert type(result) == DAGCircuit
    assert result.num_qubits() == 3
    last_node = result.op_nodes()[-1]
    assert last_node.name == "h"
    assert len(result.descendants(last_node)) == 1
    q = QuantumRegister(3, "q")
    c = ClassicalRegister(3, "c")
    circ = QuantumCircuit(q, c)
    circ.h(q[0])
    circ.cx(q[0], q[1])
    circ.h(0)

    candidate_circ = dag_to_circuit(result)
    assert Statevector.from_instruction(circ).equiv(Statevector.from_instruction(candidate_circ))
