from qiskit.circuit.library import efficient_su2
from qiskit_ibm_transpiler.transpiler_service import TranspilerService
def ai_transpiling(num_qubits):
    """ Generate an EfficientSU2 circuit with the given number of qubits, 1 reps and make entanglement circular. 
    Then use the Qiskit Transpiler service with the AI flag turned on, use the ibm_brisbane backend and an optimization level of 3 and transpile the generated circuit.
    """

    circuit = efficient_su2(num_qubits, entanglement="circular", reps=1)
    transpiler_ai_true = TranspilerService(
        backend_name="ibm_brisbane",
        ai=True,
        optimization_level=3
    )

    transpiled_circuit = transpiler_ai_true.run(circuit)
    return transpiled_circuit
