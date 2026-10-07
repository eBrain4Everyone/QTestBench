def check(candidate):
    from qiskit.primitives import StatevectorSampler
    qc = QuantumCircuit(3, 2)
    qc.x(1)
    qc.h(1)
    candidate(qc, 1, 0)

    result = StatevectorSampler().run([qc]).result()[0].data.c.get_counts()
    assert result.get('01') == 1024
