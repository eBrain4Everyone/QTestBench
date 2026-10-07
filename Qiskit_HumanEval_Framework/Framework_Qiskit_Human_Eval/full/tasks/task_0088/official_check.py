def check(candidate):
    from qiskit import QuantumRegister
    from qiskit.circuit import CircuitInstruction
    from qiskit.circuit.library import HGate
    from qiskit_aer import AerSimulator
    from qiskit_ibm_runtime import Sampler
    qr = QuantumRegister(1, name="q")
    circuit = candidate()
    data = circuit.data
    assert data[0]==CircuitInstruction(HGate(), [qr[0]], [])
    assert data[2].operation.name == "if_else"
    backend = AerSimulator()
    sampler = Sampler(mode=backend)
    results = sampler.run([circuit],shots=1024).result()
    counts= results[0].data.c.get_counts()
    assert counts == {'1': 1024}
    assert sum(counts.values()) == 1024
