from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import MatrixExponential
from qiskit import QuantumCircuit
from qiskit.quantum_info import Pauli, Operator
import numpy as np
def synthesize_evolution_gate(pauli_string: str, time: float) -> QuantumCircuit:
    """ Synthesize an evolution gate using MatrixExponential for a given Pauli string and time.
    The Pauli string can be any combination of 'I', 'X', 'Y', and 'Z'.
    Return the resulting QuantumCircuit.
    """

    pauli = Pauli(pauli_string)
    evolution_gate = PauliEvolutionGate(pauli, time)
    synthesizer = MatrixExponential()
    qc = synthesizer.synthesize(evolution_gate)
    return qc
