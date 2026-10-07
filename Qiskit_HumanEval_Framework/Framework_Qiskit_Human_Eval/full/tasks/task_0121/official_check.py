def check(candidate):
    from qiskit_aer import AerSimulator
    from qiskit_ibm_runtime import Sampler
    from qiskit_ibm_runtime.options import SamplerOptions
    qc = candidate()
    assert isinstance(qc, QuantumCircuit)
    assert qc.num_qubits == 1
    assert qc.num_clbits == 2
    ops = dict(qc.count_ops())
    assert "h" in ops and "if_else" in ops
    backend = AerSimulator()
    options = SamplerOptions()
    options.simulator.seed_simulator=42
    sampler = Sampler(mode=backend, options=options)
    result = sampler.run([qc]).result()
    counts = result[0].data.c.get_counts()
    assert "10" not in counts and "11" not in counts
