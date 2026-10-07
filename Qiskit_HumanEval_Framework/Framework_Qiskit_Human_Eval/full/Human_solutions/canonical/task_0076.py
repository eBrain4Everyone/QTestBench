from qiskit import QuantumRegister
from qiskit.transpiler.basepasses import TransformationPass
from qiskit.dagcircuit import DAGCircuit
from qiskit.circuit.library import ZGate, HGate, XGate
def create_hxh_pass() -> TransformationPass:
    """ Return a transpiler pass that replaces all non-controlled Z-gates with H-X-H-gate sequences.
    """

    class HXHPass(TransformationPass):
        def run(
            self,
            dag: DAGCircuit,
        ) -> DAGCircuit:
            for node in dag.op_nodes():
                if not isinstance(node.op, ZGate):
                    continue
                # Create HXH gate sequence
                hxh_dag = DAGCircuit()
                register = QuantumRegister(1)
                hxh_dag.add_qreg(register)

                hxh_dag.apply_operation_back(HGate(), [register[0]])
                hxh_dag.apply_operation_back(XGate(), [register[0]])
                hxh_dag.apply_operation_back(HGate(), [register[0]])

                dag.substitute_node_with_dag(node, hxh_dag)

            return dag

    return HXHPass()
