# LLM-generated solution — task_0001
# Generated: 2026-06-23T18:15:41.976166
# Model: gemini3pro
# Variant: generated_non_rag_2

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
    
    sampler = Sampler(backend=backend)
    job = sampler.run([transpiled_qc])
    result = job.result()
    
    if hasattr(result, "quasi_dists"):
        quasi_dist = result.quasi_dists[0]
        shots = 4000
        if result.metadata and len(result.metadata) > 0:
            shots = result.metadata[0].get('shots', 4000)
            
        counts = {}
        for state, prob in quasi_dist.items():
            if isinstance(state, str):
                if state.startswith("0x"):
                    key = bin(int(state, 16))[2:].zfill(transpiled_qc.num_clbits)
                else:
                    key = state
            else:
                key = bin(state)[2:].zfill(transpiled_qc.num_clbits)
            counts[key] = int(round(prob * shots))
        return counts
    else:
        return result[0].data.meas.get_counts()
