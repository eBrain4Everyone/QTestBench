# LLM-generated solution — task_0020
# Generated: 2026-06-23T18:07:23.191252
# Model: deepseekv32
# Variant: generated_non_rag_3

from qiskit import QuantumCircuit
from qiskit_ibm_runtime.fake_provider import FakePerth
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

def transpile_ghz_customlayout() -> QuantumCircuit:
    backend = FakePerth()
    
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    
    target = backend.target
    coupling_map = backend.coupling_map
    initial_layout = [2, 4, 6]
    
    pm = generate_preset_pass_manager(
        optimization_level=1,
        target=target,
        coupling_map=coupling_map,
        initial_layout=initial_layout,
        seed_transpiler=42
    )
    
    return pm.run(qc)
