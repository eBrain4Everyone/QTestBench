# LLM-generated solution — task_0001
# Generated: 2026-06-23T18:42:56.630293
# Model: gpt54
# Variant: generated_non_rag_2

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
    pass_manager = generate_preset_pass_manager(backend=backend, optimization_level=1)
    transpiled_qc = pass_manager.run(qc)

    try:
        sampler = Sampler(mode=backend)
    except TypeError:
        sampler = Sampler(backend=backend)

    job = sampler.run([transpiled_qc], shots=1024)
    result = job.result()

    pub_result = result[0]
    data = getattr(pub_result, "data", None)

    counts = None
    if data is not None:
        meas = getattr(data, "c", None)
        if meas is None:
            meas = getattr(data, "meas", None)
        if meas is not None:
            if hasattr(meas, "get_counts"):
                counts = meas.get_counts()
            elif hasattr(meas, "get_int_counts"):
                int_counts = meas.get_int_counts()
                num_bits = transpiled_qc.num_clbits
                counts = {format(k, "0{}b".format(num_bits)): v for k, v in int_counts.items()}

    if counts is None:
        quasi_dists = getattr(result, "quasi_dists", None)
        if quasi_dists is not None and len(quasi_dists) > 0:
            qd = quasi_dists[0]
            num_bits = transpiled_qc.num_clbits
            counts = {}
            for k, v in qd.items():
                if isinstance(k, int):
                    bitstring = format(k, "0{}b".format(num_bits))
                else:
                    bitstring = str(k)
                counts[bitstring] = int(round(v * 1024))

    if counts is None:
        raise RuntimeError("Unable to extract counts from sampler result.")

    return counts
