from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
def bell_each_shot() -> list[str]:
    """ Run a phi plus Bell circuit using Qiskit Sampler with the Aer simulator as backend for 100 shots and return measurement results for each shots. To do so, transpile the circuit using a pass manager with optimization level as 1.
    """

    bell = QuantumCircuit(2)
    # Apply gates
    bell.h(0)
    bell.cx(0, 1)
    bell.measure_all()

    # choose simulator backend
    backend = AerSimulator()
    # Transpile for simulator
    pass_manager = generate_preset_pass_manager(optimization_level=1, backend=backend)
    bell_circ = pass_manager.run(bell)
    sampler = Sampler(mode=backend)
    result = sampler.run([bell_circ],shots=100).result()
    memory = result[0].data.meas.get_bitstrings()
    return memory
