def check(candidate):
    from qiskit.circuit.library import CXGate
    from qiskit_aer import AerSimulator
    from qiskit_ibm_runtime import Sampler
    qc = QuantumCircuit(2, 3)
    qc.x(0)
    candidate(qc, CXGate(), [0, 1], [0, 2])
    qc.measure_all()
    sampler = Sampler(mode=AerSimulator())
    result = sampler.run([qc]).result()[0].data.meas.get_counts()
    assert result.get("01") == 1024

    qc = QuantumCircuit(2, 3)
    qc.x([0, 1])
    qc.measure([0, 1], [0, 2])
    qc.x(1)
    candidate(qc, CXGate(), [0, 1], [0, 2])
    qc.measure_all()

    result = sampler.run([qc]).result()[0].data.meas.get_counts()
    assert result.get("11") == 1024
