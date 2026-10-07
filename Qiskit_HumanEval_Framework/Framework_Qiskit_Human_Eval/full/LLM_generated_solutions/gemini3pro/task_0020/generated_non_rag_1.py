# LLM-generated solution — task_0020
# Generated: 2026-06-23T18:21:48.242095
# Model: gemini3pro
# Variant: generated_non_rag_1

from qiskit import QuantumCircuit
from qiskit_ibm_runtime.fake_provider import FakePerth
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

def transpile_ghz_customlayout() -> QuantumCircuit:
    """ Using a pass manager with optimization level as 1, transpile and map a three-qubit GHZ circuit for the Fake Perth backend using custom initial layout: [2,4,6].
    """
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    
    backend = FakePerth()
    pass_manager = generate_preset_pass_manager(
        optimization_level=1,
        backend=backend,
        initial_layout=[2, 4, 6]
    )
    
    transpiled_qc = pass_manager.run(qc)
    return transpiled_qc
