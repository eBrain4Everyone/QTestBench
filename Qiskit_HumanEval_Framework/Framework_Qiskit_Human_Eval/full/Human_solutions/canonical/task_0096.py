from qiskit_ibm_runtime.fake_provider import FakeKyoto
from qiskit.circuit import QuantumCircuit
from qiskit_ibm_runtime import Sampler
from qiskit_ibm_runtime.options import SamplerOptions
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
def bell_state_noisy() -> dict:
    """ Create the phi+ Bell state, run it in the FakeKyoto backend and return the counts. Use seed 42 for the sampler.
    """

    backend = FakeKyoto()
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    pass_manager = generate_preset_pass_manager(optimization_level=1, backend=backend)
    isa_circuit = pass_manager.run(qc)
    options = SamplerOptions()
    options.simulator.seed_simulator=42
    sampler = Sampler(backend, options=options)
    result = sampler.run([isa_circuit]).result()
    counts = result[0].data.meas.get_counts()
    return counts
