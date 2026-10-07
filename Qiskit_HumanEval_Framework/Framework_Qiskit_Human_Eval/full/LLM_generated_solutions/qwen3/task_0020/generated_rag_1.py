# LLM-generated solution — task_0020
# Generated: 2026-06-23T18:50:58.811015
# Model: qwen3
# Variant: generated_rag_1

from qiskit import QuantumCircuit
from qiskit_ibm_runtime.fake_provider import FakePerth
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

def transpile_ghz_customlayout() -> QuantumCircuit:
    """ Using a pass manager with optimization level as 1, transpile and map a three-qubit GHZ circuit for the Fake Perth backend using custom initial layout: [2,4,6].
    """
    # Create a three-qubit GHZ circuit
    ghz_circuit = QuantumCircuit(3)
    ghz_circuit.h(0)
    ghz_circuit.cx(0, 1)
    ghz_circuit.cx(0, 2)
    
    # Get the FakePerth backend
    backend = FakePerth()
    
    # Create a preset pass manager with optimization level 1
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    
    # Set the initial layout to map logical qubits [0,1,2] to physical qubits [2,4,6]
    initial_layout = [2, 4, 6]
    pm.layout = initial_layout
    
    # Transpile the circuit with the custom layout
    transpiled_circuit = pm.run(ghz_circuit)
    
    return transpiled_circuit
