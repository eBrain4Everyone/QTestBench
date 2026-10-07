# LLM-generated solution — task_0020
# Generated: 2026-06-23T18:44:49.682132
# Model: gpt54
# Variant: generated_non_rag_2

from qiskit import QuantumCircuit
from qiskit_ibm_runtime.fake_provider import FakePerth
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

def transpile_ghz_customlayout() -> QuantumCircuit:
    """ Using a pass manager with optimization level as 1, transpile and map a three-qubit GHZ circuit for the Fake Perth backend using custom initial layout: [2,4,6].
    """
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(0, 2)

    backend = FakePerth()
    pm = generate_preset_pass_manager(
        optimization_level=1,
        backend=backend,
        initial_layout=[2, 4, 6],
    )
    transpiled_qc = pm.run(qc)
    return transpiled_qc
