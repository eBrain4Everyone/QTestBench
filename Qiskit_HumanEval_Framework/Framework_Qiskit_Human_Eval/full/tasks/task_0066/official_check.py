def check(candidate):
    from qiskit_aer import AerSimulator
    from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
    from qiskit_ibm_runtime import Sampler
    result = candidate()
    assert isinstance(result, QuantumCircuit)
    assert result.num_qubits == 3
    backend = AerSimulator()
    sampler = Sampler(mode=backend)
    pass_manager = generate_preset_pass_manager(optimization_level=1, backend=backend)
    isa_circuit = pass_manager.run(result)
    job = sampler.run([isa_circuit]).result()
    counts= job[0].data.meas.get_counts()
    assert counts.keys() == {'001', '010' , '100'}
    assert counts['001'] >= 300 and counts['001'] <= 400
    assert counts['010'] >= 300 and counts['010'] <= 400
    assert counts['100'] >= 300 and counts['100'] <= 400
    assert counts['001'] + counts['010'] + counts['100'] == 1024
