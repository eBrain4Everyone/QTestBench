from qiskit_ibm_runtime.fake_provider import FakeCairoV2
from qiskit.transpiler import CouplingMap
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
def transpile_circuit(circuit: QuantumCircuit) -> QuantumCircuit:
    """ For the given Quantum Circuit, return the transpiled circuit for the Fake Cairo V2 backend using pass manager with optimization level as 1.
    """

    backend = FakeCairoV2()
    coupling_map = CouplingMap(backend.configuration().coupling_map)
    pass_manager = generate_preset_pass_manager(optimization_level=1, backend=backend, coupling_map=coupling_map)
    return pass_manager.run(circuit)
