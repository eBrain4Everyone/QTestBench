from qiskit import QuantumCircuit
from qiskit.transpiler.passes import CollectLinearFunctions
from qiskit.transpiler import PassManager
def collect_linear_blocks_with_and_without_limit():
    """ Create a 5-qubit quantum circuit with a chain of CX gates and apply Qiskit's CollectLinearFunctions transpiler pass. Return two circuits:
    1. One with no block width restriction.
    2. One with a max_block_width of 3.
    Use PassManager to apply the pass and return both circuits.
    """

    qc = QuantumCircuit(5)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.cx(2, 3)
    qc.cx(3, 4)
    pm_full = PassManager([CollectLinearFunctions()])
    full_block = pm_full.run(qc)
    pm_limited = PassManager([CollectLinearFunctions(max_block_width=3)])
    limited_block = pm_limited.run(qc)
    return full_block, limited_block
