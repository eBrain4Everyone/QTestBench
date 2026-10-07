# LLM-generated solution — task_0001
# Generated: 2026-06-23T18:16:57.905087
# Model: gemini3pro
# Variant: generated_non_rag_3

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

def run_bell_state_simulator():
    """ Define a phi plus bell state using Qiskit, transpile the circuit using pass manager with optimization level as 1, run it using Qiskit Sampler with the Aer simulator as backend and return the counts dictionary.
    """
    # Define a phi plus bell state
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    
    # Transpile the circuit using pass manager with optimization level 1
    backend = AerSimulator()
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled_qc = pm.run(qc)
    
    # Run it using Qiskit Sampler with the Aer simulator as backend
    sampler = Sampler(backend=backend)
    shots = 1024
    job = sampler.run(transpiled_qc, shots=shots)
    result = job.result()
    
    # Convert quasi-distributions to counts dictionary
    quasi_dist = result.quasi_dists[0]
    probs = quasi_dist.binary_probabilities(num_bits=2)
    counts = {state: int(round(prob * shots)) for state, prob in probs.items()}
    
    return counts
