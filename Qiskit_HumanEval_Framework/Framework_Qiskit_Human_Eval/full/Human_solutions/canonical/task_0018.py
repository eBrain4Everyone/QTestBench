from qiskit import QuantumCircuit
from qiskit_ibm_runtime.fake_provider import FakeSydneyV2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
def transpile_circuit_noopt() -> QuantumCircuit:
    """ Transpile a 10-qubit GHZ circuit for the Fake Sydney V2 backend using pass manager with no optimization.
    """

    backend = FakeSydneyV2()
    ghz = QuantumCircuit(10)
    ghz.h(0)
    ghz.cx(0, range(1, 10))
    ghz.measure_all()
    pass_manager = generate_preset_pass_manager(optimization_level=0, backend=backend)
    return pass_manager.run(ghz)
