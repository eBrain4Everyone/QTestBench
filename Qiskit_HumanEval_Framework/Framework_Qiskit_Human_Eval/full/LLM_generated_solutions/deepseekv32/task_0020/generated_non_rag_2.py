# LLM-generated solution — task_0020
# Generated: 2026-06-23T18:07:15.357994
# Model: deepseekv32
# Variant: generated_non_rag_2

from qiskit import QuantumCircuit
from qiskit_ibm_runtime.fake_provider import FakePerth
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

def transpile_ghz_customlayout() -> QuantumCircuit:
    backend = FakePerth()
    pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
    
    ghz_circuit = QuantumCircuit(3)
    ghz_circuit.h(0)
    ghz_circuit.cx(0, 1)
    ghz_circuit.cx(0, 2)
    
    ghz_circuit.measure_all()
    
    initial_layout = [2, 4, 6]
    
    transpiled_circuit = pm.run(ghz_circuit, initial_layout=initial_layout)
    
    return transpiled_circuit
