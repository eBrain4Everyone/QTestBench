# LLM-generated solution — task_0001
# Generated: 2026-06-23T18:43:06.356072
# Model: gpt54
# Variant: generated_non_rag_3

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

def run_bell_state_simulator():
    """ Define a phi plus bell state using Qiskit, transpile the circuit using pass manager with optimization level as 1, run it using Qiskit Sampler with the Aer simulator as backend and return the counts dictionary.
    """
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])

    backend = AerSimulator()
    pass_manager = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled_qc = pass_manager.run(qc)

    try:
        sampler = Sampler(mode=backend)
    except TypeError:
        sampler = Sampler(backend=backend)

    shots = 1024
    try:
        job = sampler.run([transpiled_qc], shots=shots)
    except TypeError:
        job = sampler.run([transpiled_qc])

    result = job.result()
    pub_result = result[0]

    counts = None

    if hasattr(pub_result, "data") and hasattr(pub_result.data, "c"):
        try:
            counts = pub_result.data.c.get_counts()
        except Exception:
            counts = None

    if counts is None and hasattr(pub_result, "quasi_dists"):
        quasi = pub_result.quasi_dists[0]
        counts = {}
        for key, value in quasi.items():
            if isinstance(key, int):
                bitstring = format(key, "02b")
            else:
                bitstring = str(key)
            counts[bitstring] = int(round(value * shots))

    if counts is None:
        raise RuntimeError("Unable to extract counts from sampler result.")

    return counts
