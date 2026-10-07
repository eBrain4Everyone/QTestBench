from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
def circuit_to_bools(circuit: QuantumCircuit) -> list[bool]:
    """ Given a QuantumCircuit, sample it once and convert the measurement result to a list of bools, where the 0th bool is the result of the 0th classical bit.
    """

    result = StatevectorSampler().run([circuit], shots=1).result()[0].data.meas.get_counts()
    measurement_int = int(list(result.keys())[0], 2)
    output = []
    for bit_index in range(circuit.num_clbits):
        # Use bit-masking to get bits from `int`
        bit = bool(2 ** (bit_index) & measurement_int)
        output.append(bit)
    return output
