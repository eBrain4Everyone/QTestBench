def check(candidate):
    from qiskit.quantum_info import hellinger_fidelity
    counts_can = candidate()
    backend = FakeKyoto()
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    pass_manager = generate_preset_pass_manager(optimization_level=1, backend=backend)
    isa_circuit = pass_manager.run(qc)
    sampler = Sampler(backend)
    result = sampler.run([isa_circuit]).result()
    counts_exp = result[0].data.meas.get_counts()
    assert isinstance(counts_can, dict), "Return the counts"
    assert 0.7 < hellinger_fidelity(counts_can, counts_exp) < 1, "Output doesn't match with the results from Fake Kyoto"
