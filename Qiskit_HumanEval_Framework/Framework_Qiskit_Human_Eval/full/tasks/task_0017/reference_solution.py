from qiskit import QuantumCircuit
from qiskit.circuit.library.standard_gates.equivalence_library import ( StandardEquivalenceLibrary as std_eqlib, )
from qiskit.transpiler.passes import BasisTranslator
from qiskit.transpiler import PassManager
import numpy as np
def unroll_circuit(circuit: QuantumCircuit) -> QuantumCircuit:
    """ Unroll circuit for the gateset: CX, ID, RZ, SX, X, U.
    """

    pass_ = BasisTranslator(std_eqlib, ["cx", "id", "rz", "sx", "x", "u"])
    pm = PassManager(pass_)
    return pm.run(circuit)
