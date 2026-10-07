# LLM-generated solution — task_0001
# Generated: 2026-06-23T18:14:10.384903
# Model: gemini3pro
# Variant: generated_non_rag_1

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
    
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled_qc = pm.run(qc)
    
    shots = 1024
    sampler = Sampler(backend=backend, options={"shots": shots})
    result = sampler.run(transpiled_qc).result()
    
    quasi_dist = result.quasi_dists[0]
    
    if hasattr(quasi_dist, 'binary_probabilities'):
        probs = quasi_dist.binary_probabilities(num_bits=2)
    else:
        probs = {format(k, '02b'): v for k, v in quasi_dist.items()}
        
    counts = {k: int(round(v * shots)) for k, v in probs.items()}
    
    return counts
