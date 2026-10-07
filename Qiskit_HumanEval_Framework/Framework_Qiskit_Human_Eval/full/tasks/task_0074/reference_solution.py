from qiskit import QuantumCircuit
from qiskit.circuit.library import Barrier
def split_circuit_at_barriers(circuit: QuantumCircuit) -> list[QuantumCircuit]:
    """ Split `circuit` at each barrier operation. Do not include barriers in the output circuits.
    """

    output = []
    new_circuit = circuit.copy_empty_like()
    for inst in circuit.data:
        if isinstance(inst.operation, Barrier):
            output.append(new_circuit)
            new_circuit = circuit.copy_empty_like()
            continue
        new_circuit.data.append(inst)
    output.append(new_circuit)
    return output
