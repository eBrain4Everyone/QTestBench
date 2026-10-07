from qiskit import QuantumCircuit
from qiskit_ibm_runtime.fake_provider import FakeTorontoV2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
def transpile_circuit_maxopt() -> QuantumCircuit:
    """ Transpile and map an 11-qubit GHZ circuit for the Fake Toronto V2 backend using pass manager with maximum transpiler optimization.
    """

    backend = FakeTorontoV2()
    ghz = QuantumCircuit(11)
    ghz.h(0)
    ghz.cx(0, range(1, 11))
    ghz.barrier()
    pass_manager = generate_preset_pass_manager(optimization_level=3, backend=backend)
    return pass_manager.run(ghz)
