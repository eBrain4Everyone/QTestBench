# LLM-generated solution — task_0020
# Generated: 2026-06-23T18:06:45.507965
# Model: deepseekv32
# Variant: generated_non_rag_1

from qiskit import QuantumCircuit
from qiskit_ibm_runtime.fake_provider import FakePerth
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

def transpile_ghz_customlayout() -> QuantumCircuit:
    """ Using a pass manager with optimization level as 1, transpile and map a three-qubit GHZ circuit for the Fake Perth backend using custom initial layout: [2,4,6].
    """
    backend = FakePerth()
    pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
    ghz = QuantumCircuit(3)
    ghz.h(0)
    ghz.cx(0, 1)
    ghz.cx(0, 2)
    ghz.measure_all()
    transpiled = pm.run(ghz, initial_layout=[2, 4, 6])
    return transpiled
