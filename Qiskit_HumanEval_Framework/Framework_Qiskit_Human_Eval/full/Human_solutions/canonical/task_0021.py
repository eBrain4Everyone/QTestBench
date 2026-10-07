from qiskit import QuantumCircuit
from qiskit_ibm_runtime.fake_provider import FakeOslo
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
def transpile_circuit_dense() -> QuantumCircuit:
    """ Using a pass manager with optimization level as 1 and dense layout method, transpile and map a bell circuit for the Fake Oslo backend.
    """

    backend = FakeOslo()
    bell = QuantumCircuit(2)
    bell.h(0)
    bell.cx(0, 1)
    pass_manager = generate_preset_pass_manager(optimization_level=1, backend=backend, layout_method="dense")
    solution_circ = pass_manager.run(bell)
    return solution_circ
