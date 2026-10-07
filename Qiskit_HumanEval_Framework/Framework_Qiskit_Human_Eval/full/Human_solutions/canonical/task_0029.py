from matplotlib.figure import Figure
from qiskit.visualization import plot_circuit_layout
from qiskit import QuantumCircuit
from qiskit_ibm_runtime.fake_provider import FakeAthensV2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
def plot_circuit_layout_bell() -> Figure:
    """ Plot a circuit layout visualization for a transpiled bell circuit using a pass manager with optimization level as 1 for the Fake Athens V2 backend.
    """

    backend = FakeAthensV2()
    bell = QuantumCircuit(2)
    bell.h(0)
    bell.cx(0,1)
    pass_manager = generate_preset_pass_manager(optimization_level=1, backend=backend)
    brisbane_bell = pass_manager.run(bell)
    return (plot_circuit_layout(brisbane_bell, backend))
