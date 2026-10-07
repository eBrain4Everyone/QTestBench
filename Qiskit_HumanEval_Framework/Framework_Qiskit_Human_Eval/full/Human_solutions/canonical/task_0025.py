from qiskit import QuantumCircuit
from qiskit.transpiler import CouplingMap
from qiskit.transpiler.passes import LookaheadSwap
from qiskit.transpiler.passmanager import PassManager
def passmanager_Lookahead(coupling) -> QuantumCircuit:
    """ Transpile a 7-qubit GHZ circuit using LookaheadSwap pass and the input custom coupling map.
    """

    ghz = QuantumCircuit(7)
    ghz.h(0)
    ghz.cx(0, range(1, 7))
    coupling_map = CouplingMap(couplinglist=coupling)
    ls = LookaheadSwap(coupling_map=coupling_map)
    pass_manager = PassManager(ls)
    lookahead_circ = pass_manager.run(ghz)
    return lookahead_circ
