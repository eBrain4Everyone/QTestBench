from qiskit.circuit import QuantumCircuit
from qiskit.quantum_info.operators import Operator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
def create_operator() -> QuantumCircuit:
    """ Create a Qiskit circuit with the following unitary [[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]], consisting of only single-qubit gates and CX gates, then transpile the circuit using pass manager with optimization level as 1.
    """

    XX = Operator([[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]])
    circ = QuantumCircuit(2, 2)
    circ.append(XX, [0, 1])
    pass_manager = generate_preset_pass_manager(optimization_level=1, basis_gates=["u", "cx"])
    return pass_manager.run(circ)
