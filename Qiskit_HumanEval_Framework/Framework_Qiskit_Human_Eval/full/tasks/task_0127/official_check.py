def check(candidate):
    from qiskit.circuit.random import random_circuit
    from qiskit import QuantumCircuit

    # Run the candidate function
    result = candidate()

    # Check if the output is a QuantumCircuit
    assert isinstance(result, QuantumCircuit), "Output should be a QuantumCircuit"

    # Generate the expected circuit using the same parameters
    expected_qc = random_circuit(4, 3, measure=True, seed=17)

    # Ensure the circuit has 4 qubits
    assert result.num_qubits == 4, f"Expected 4 qubits, but got {result.num_qubits}"

    # Ensure the circuit depth is within an acceptable range (allowing small variations)
    expected_depth = expected_qc.depth()
    assert abs(result.depth() - expected_depth) <= 1, f"Expected depth around {expected_depth}, but got {result.depth()}"

    # Check if all qubits are measured at the end
    measured_qubits = [inst for inst in result.data if inst.operation.name == "measure"]
    assert len(measured_qubits) == 4, "All qubits should be measured at the end"

    # Ensure the generated circuit matches the expected circuit structure
    assert result == expected_qc, "Generated circuit does not match expected circuit"
