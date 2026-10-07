def check(candidate):
    from qiskit_aer import AerSimulator
    from qiskit_ibm_runtime import Sampler
    result_1 = candidate("10")
    backend = AerSimulator()
    sampler = Sampler(mode=backend)
    assert isinstance(result_1, QuantumCircuit)
    assert result_1.num_qubits == 2
    assert result_1.count_ops()["x"] == 1
    assert sampler.run([result_1]).result()[0].data.measure.get_counts() == {"10": 1024}
    result_2 = candidate("01")
    assert result_2.depth() == 6
    assert result_2.count_ops()["z"] == 1
    assert sampler.run([result_2]).result()[0].data.measure.get_counts() == {"01": 1024}
