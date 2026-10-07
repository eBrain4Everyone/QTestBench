from qiskit import QuantumCircuit
def create_ghz(drawing=False):
    """ Generate a QuantumCircuit for a 3 qubit GHZ State and measure it. If `drawing` is True, return both the circuit object and the Matplotlib drawing of the circuit, otherwise return just the circuit object.
    """

    ghz = QuantumCircuit(3)
    ghz.h(0)
    ghz.cx(0, 1)
    ghz.cx(0, 2)
    ghz.measure_all()
    if drawing:
        return ghz, ghz.draw(output="mpl")
    return ghz