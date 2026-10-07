def check(candidate):
    import qiskit
    from qiskit.circuit.library import efficient_su2
    num_qubits = 3
    backend_name = "ibm_brisbane"
    ai_flag = True
    optimization_level = 3
    og_circuit = efficient_su2(num_qubits, entanglement="circular", reps=1)
    gen_transpiled_circuit = candidate(num_qubits)
    assert isinstance(gen_transpiled_circuit, qiskit.circuit.QuantumCircuit)
    transpiler_service = TranspilerService(
        backend_name=backend_name,
        ai=ai_flag,
        optimization_level=optimization_level
    )

    expected_transpiled_circuit = transpiler_service.run(og_circuit)

    # We can add the following check once we have the random_state/seed feature in the transpiler service
    # assert gen_transpiled_circuit == expected_transpiled_circuit
