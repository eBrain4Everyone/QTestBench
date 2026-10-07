from qiskit.dagcircuit import DAGCircuit
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.converters import circuit_to_dag
def bell_dag() -> DAGCircuit:
    """ Construct a DAG circuit for a 3-qubit Quantum Circuit with the bell state applied on qubit 0 and 1. Finally return the DAG Circuit object.
    """

    q = QuantumRegister(3, 'q')
    c = ClassicalRegister(3, 'c')
    circ = QuantumCircuit(q, c)
    circ.h(q[0])
    circ.cx(q[0], q[1])
    circ.measure(q[0], c[0])
    dag = circuit_to_dag(circ)
    return dag
