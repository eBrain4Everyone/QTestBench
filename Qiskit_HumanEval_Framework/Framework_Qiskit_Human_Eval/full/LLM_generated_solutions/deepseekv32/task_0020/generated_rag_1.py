# LLM-generated solution — task_0020
# Generated: 2026-06-23T18:07:33.950053
# Model: deepseekv32
# Variant: generated_rag_1

from qiskit import QuantumCircuit
from qiskit_ibm_runtime.fake_provider import FakePerth
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

def transpile_ghz_customlayout() -> QuantumCircuit:
    """ Using a pass manager with optimization level as 1, transpile and map a three-qubit GHZ circuit for the Fake Perth backend using custom initial layout: [2,4,6].
    """
    # Create a 3-qubit GHZ circuit
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(0,__)
    
    # Create backend
    backend = FakePerth()
    
    # Create pass manager with optimization level 1
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    
    # Set custom initial layout [2,4,6]
    initial_layout = [2, 4, 6]
    
    # Transpile with custom layout
    transpiled_qc = pm.run(qc, initial_layout=initial_layout)
    
    return transpiled_qc
