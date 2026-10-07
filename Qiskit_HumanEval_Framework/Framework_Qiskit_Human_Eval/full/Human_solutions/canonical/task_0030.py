from qiskit import QuantumCircuit
from matplotlib.figure import Figure
from qiskit.visualization import plot_state_city
from qiskit.quantum_info import Statevector
def plot_circuit_layout_bell() -> Figure:
    """ Plot a city_state for a bell circuit.
    """

    bell = QuantumCircuit(2)
    bell.h(0)
    bell.cx(0,1)
    bell_state = Statevector(bell)
    plot_state_city(bell_state)
    return plot_state_city(bell_state)
