import contextlib
from qiskit import QuantumCircuit
from qiskit.circuit import Gate
def gate_if_clbits(
    circuit: QuantumCircuit, gate: Gate, qubits: list[int], condition_clbits: list[int]
) -> None:
    """ Apply `gate` to qubits with indices `qubits`, conditioned on all `condition_clbits` being 1.
    """

    with contextlib.ExitStack() as stack:
        for index in condition_clbits:
            stack.enter_context(circuit.if_test((index, 1)))
        circuit.append(gate, qubits)
