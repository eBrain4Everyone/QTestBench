# LLM-generated solution — task_0019
# Generated: 2026-06-23T18:44:26.904056
# Model: gpt54
# Variant: generated_non_rag_3

from qiskit import QuantumCircuit
from qiskit_ibm_runtime.fake_provider import FakeTorontoV2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

def transpile_circuit_maxopt() -> QuantumCircuit:
    """ Transpile and map an 11-qubit GHZ circuit for the Fake Toronto V2 backend using pass manager with maximum transpiler optimization.
    """
    qc = QuantumCircuit(11)
    qc.h(0)
    for i in range(10):
        qc.cx(i, i + 1)
    qc.measure_all()

    backend = FakeTorontoV2()
    pass_manager = generate_preset_pass_manager(backend=backend, optimization_level=3)
    transpiled = pass_manager.run(qc)
    return transpiled
