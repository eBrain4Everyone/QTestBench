from qiskit import QuantumCircuit
from qiskit.transpiler.passes import BasicSwap
from qiskit.converters import circuit_to_dag, dag_to_circuit
from qiskit_ibm_runtime import IBMBackend
def swap_map(qc: QuantumCircuit, backend: IBMBackend) -> QuantumCircuit:
    """ Add SWAPs to route `qc` for the `backend` object's coupling map, but don't transform any gates.
    """

    swap_pass = BasicSwap(coupling_map=backend.coupling_map)
    dag = circuit_to_dag(qc)
    mapped_dag = swap_pass.run(dag)
    return dag_to_circuit(mapped_dag)
