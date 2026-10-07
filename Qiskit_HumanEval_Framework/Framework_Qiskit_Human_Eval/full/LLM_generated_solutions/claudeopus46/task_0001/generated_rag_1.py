# LLM-generated solution — task_0001
# Generated: 2026-06-23T17:55:45.708861
# Model: claudeopus46
# Variant: generated_rag_1

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

def run_bell_state_simulator():
    """ Define a phi plus bell state using Qiskit, transpile the circuit using pass manager with optimization level as 1, run it using Qiskit Sampler with the Aer simulator as backend and return the counts dictionary.
    """
    # Create the Bell state |_+_ = (|00_ + |11_) / _2
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    # Set up the Aer simulator backend
    backend = AerSimulator()

    # Transpile the circuit using a preset pass manager with optimization level 1
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled_circuit = pm.run(qc)

    # Run using Sampler with the Aer simulator backend
    sampler = Sampler(mode=backend)
    job = sampler.run([transpiled_circuit])
    result = job.result()

    # Extract counts from the result
    pub_result = result[0]
    counts = pub_result.data.meas.get_counts()

    return counts
