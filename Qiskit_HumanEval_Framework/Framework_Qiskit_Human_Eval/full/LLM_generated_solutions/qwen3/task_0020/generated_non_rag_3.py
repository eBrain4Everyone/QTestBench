# LLM-generated solution — task_0020
# Generated: 2026-06-23T18:50:53.949781
# Model: qwen3
# Variant: generated_non_rag_3

from qiskit import QuantumCircuit
from qiskit_ibm_runtime.fake_provider import FakePerth
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.transpiler import Layout

def transpile_ghz_customlayout() -> QuantumCircuit:
    """ Using a pass manager with optimization level as 1, transpile and map a three-qubit GHZ circuit for the Fake Perth backend using custom initial layout: [2,4,6].
    """
    # Create a three-qubit GHZ circuit
    ghz_circuit = QuantumCircuit(3)
    ghz_circuit.h(0)
    ghz_circuit.cx(0, 1)
    ghz_circuit.cx(0, 2)
    
    # Get the Fake Perth backend
    backend = FakePerth()
    
    # Create custom initial layout: [2, 4, 6] mapping logical qubits 0, 1, 2 to physical qubits
    initial_layout = Layout({0: 2, 1: 4, 2: 6})
    
    # Generate preset pass manager with optimization level 1
    pass_manager = generate_preset_pass_manager(
        optimization_level=1,
        backend=backend,
        initial_layout=initial_layout
    )
    
    # Transpile the GHZ circuit
    transpiled_circuit = pass_manager.run(ghz_circuit)
    
    return transpiled_circuit
