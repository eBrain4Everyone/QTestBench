from matplotlib.figure import Figure
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
from qiskit.visualization import plot_histogram
def visualize_bell_states()->Figure:
    """ Prepare phi plus and phi minus bell states and visualize their results in a histogram and return the histogram.
    """

    phi_plus = QuantumCircuit(2)
    phi_minus = QuantumCircuit(2)
    phi_plus.h(0)
    phi_plus.cx(0,1)
    phi_minus.x(0)
    phi_minus.h(0)
    phi_minus.cx(0,1)
    phi_plus.measure_all()
    phi_minus.measure_all()
    backend = AerSimulator()
    sampler = Sampler(mode=backend)
    result_phi_plus = sampler.run([phi_plus], shots=1000).result()
    result_phi_minus = sampler.run([phi_minus], shots=1000).result()
    phi_plus_counts = result_phi_plus[0].data.meas.get_counts()
    phi_minus_counts = result_phi_minus[0].data.meas.get_counts()
    return plot_histogram([phi_plus_counts, phi_minus_counts], legend = ['|Φ+⟩ Count', '|Φ-⟩ Count'])
