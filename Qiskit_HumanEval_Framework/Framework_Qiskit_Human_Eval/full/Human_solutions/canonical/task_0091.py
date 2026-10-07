from qiskit import QuantumCircuit
from qiskit.converters import circuit_to_instruction
def convert_circuit_to_instruction():
    """ Create a circuit that produces a phi plus bell state with name bell_instruction and convert it into a quantum instruction.
    """

    circ = QuantumCircuit(2, 2, name="bell_instruction")
    circ.h(0)
    circ.cx(0,1)
    circ.measure([0, 1], [0, 1])
    instruction = circuit_to_instruction(circ)
    return instruction
