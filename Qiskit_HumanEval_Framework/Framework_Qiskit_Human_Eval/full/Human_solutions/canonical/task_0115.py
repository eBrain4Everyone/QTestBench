from qiskit.transpiler import Target, InstructionProperties
from qiskit.circuit.library import UGate, CXGate
from qiskit.circuit import Parameter
def create_target() -> Target:
    """ Create a Target object for a 2-qubit system and add UGate and CXGate instructions with specific properties.
    - Add UGate for both qubits (0 and 1) with parameters 'theta', 'phi', and 'lambda'.
    - Add CXGate for qubit pairs (0,1) and (1,0).
    - All instructions should have nonzero 'duration' and 'error' properties set.
    """

    gmap = Target()
    theta, phi, lam = [Parameter(p) for p in ("theta", "phi", "lambda")]
    u_props = {
        (0,): InstructionProperties(duration=5.23e-8, error=0.00038115),
        (1,): InstructionProperties(duration=4.52e-8, error=0.00032115),
    }
    gmap.add_instruction(UGate(theta, phi, lam), u_props)
    cx_props = {
        (0,1): InstructionProperties(duration=5.23e-7, error=0.00098115),
        (1,0): InstructionProperties(duration=4.52e-7, error=0.00132115),
    }
    gmap.add_instruction(CXGate(), cx_props)
    return gmap
