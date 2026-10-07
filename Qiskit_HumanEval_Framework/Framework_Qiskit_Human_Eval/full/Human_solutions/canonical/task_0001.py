from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
def run_bell_state_simulator():
    """ Define a phi plus bell state using Qiskit, transpile the circuit using pass manager with optimization level as 1, run it using Qiskit Sampler with the Aer simulator as backend and return the counts dictionary.
    """

    bell = QuantumCircuit(2)
    bell.h(0)
    bell.cx(0, 1)
    bell.measure_all()
    backend = AerSimulator()
    pass_manager = generate_preset_pass_manager(optimization_level=1, backend=backend)
    isa_circuit = pass_manager.run(bell)
    sampler = Sampler(mode=backend)
    result = sampler.run([isa_circuit], shots=1000).result()
    return result[0].data.meas.get_counts()
