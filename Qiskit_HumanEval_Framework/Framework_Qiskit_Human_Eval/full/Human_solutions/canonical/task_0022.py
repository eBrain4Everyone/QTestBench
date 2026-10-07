from qiskit import QuantumCircuit
from qiskit_ibm_runtime.fake_provider import FakeAuckland
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
def transpile_circuit_alap() -> QuantumCircuit:
    """ Using a pass manager with optimization level as 1 and as-late-as-possible scheduling method, transpile and map a bell circuit for the Fake Auckland backend. Return the circuit.
    """

    backend = FakeAuckland()
    bell = QuantumCircuit(2)
    bell.h(0)
    bell.cx(0, 1)
    pass_manager = generate_preset_pass_manager(optimization_level=1, backend=backend, scheduling_method="alap")
    return pass_manager.run(bell)
