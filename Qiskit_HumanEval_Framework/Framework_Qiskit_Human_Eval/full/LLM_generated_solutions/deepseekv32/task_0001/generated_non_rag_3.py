# LLM-generated solution — task_0001
# Generated: 2026-06-23T18:02:51.705533
# Model: deepseekv32
# Variant: generated_non_rag_3

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

def run_bell_state_simulator():
    """ Define a phi plus bell state using Qiskit, transpile the circuit using pass manager with optimization level as 1, run it using Qiskit Sampler with the Aer simulator as backend and return the counts dictionary.
    """
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    backend = AerSimulator()
    pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
    transpiled_circuit = pm.run(qc)
    sampler = Sampler(backend=backend)
    job = sampler.run(transpiled_circuit, shots=1024)
    result = job.result()
    counts = result.quasi_dists[0]
    integer_counts = {int(k): int(v * 1024) for k, v in counts.items()}
    return integer_counts
