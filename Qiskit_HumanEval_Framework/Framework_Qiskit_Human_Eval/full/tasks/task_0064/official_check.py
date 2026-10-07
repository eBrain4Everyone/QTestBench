def check(candidate):
    from qiskit_aer import AerSimulator
    from qiskit_ibm_runtime import Sampler
    result = candidate('1010')
    assert isinstance(result, QuantumCircuit)
    assert result.num_qubits == 8
    def dpm2(vec1, vec2):
        return sum(int(a) * int(b) for a, b in zip(vec1, vec2)) % 2
    backend = AerSimulator()
    sampler = Sampler(mode=backend)
    job = sampler.run([result]).result()
    data = job[0].data
    counts= data.c.get_counts()
    for key in counts:
        assert dpm2(key, "1010") == 0
