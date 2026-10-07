from typing import Dict
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
from qiskit_ibm_runtime.options import SamplerOptions
def sampler_qiskit() -> Dict:
    """ Run a Bell circuit on Qiskit Sampler and run the circuit on the Aer simulator with the seed set as 42. Return the resulting counts dictionary.
    """

    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0,1)
    qc.measure_all()

    options = SamplerOptions()
    options.simulator.seed_simulator=42
    sampler = Sampler(mode=AerSimulator(), options=options)
    job = sampler.run([qc])
    result = job.result()[0].data.meas.get_counts()
    return result
