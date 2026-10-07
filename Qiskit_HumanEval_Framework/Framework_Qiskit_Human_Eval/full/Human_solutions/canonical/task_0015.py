from qiskit_ibm_runtime.fake_provider import FakeBelemV2
from qiskit_ibm_runtime import Sampler
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
def noisy_bell():
    """ Transpile a bell circuit using pass manager with optimization level as 1, run it using Qiskit Sampler with the Aer simulator as backend and get the execution counts.
    """

    bell = QuantumCircuit(2)
    bell.h(0)
    bell.cx(0, 1)
    bell.measure_all()
    device_backend = FakeBelemV2()
    simulator = AerSimulator.from_backend(device_backend)
    pass_manager = generate_preset_pass_manager(optimization_level=1, backend=simulator)
    bell_circ = pass_manager.run(bell)
    sampler = Sampler(mode=simulator)
    result = sampler.run([bell_circ], shots=1000).result()
    counts = result[0].data.meas.get_counts()
    return counts
