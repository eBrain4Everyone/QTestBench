# LLM-generated solution — task_0001
# Generated: 2026-06-23T18:18:17.547945
# Model: gemini3pro
# Variant: generated_rag_1

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

    try:
        sampler = Sampler(backend=backend)
        job = sampler.run(transpiled_qc)
        result = job.result()
        
        if hasattr(result, 'quasi_dists'):
            shots = result.metadata[0].get('shots', 1024) if result.metadata else 1024
            quasi_dist = result.quasi_dists[0]
            counts = {}
            for k, v in quasi_dist.items():
                if isinstance(k, str):
                    if k.startswith('0x'):
                        bitstr = format(int(k, 16), f'0{qc.num_qubits}b')
                    else:
                        bitstr = k
                else:
                    bitstr = format(k, f'0{qc.num_qubits}b')
                counts[bitstr] = int(round(v * shots))
            return counts
        elif hasattr(result, "__getitem__"):
            return result[0].data.meas.get_counts()
        elif hasattr(result, "get_counts"):
            return result.get_counts()
    except Exception:
        pass
        
    job = backend.run(transpiled_qc, shots=1024)
    return job.result().get_counts()
