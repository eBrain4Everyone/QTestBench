def check(candidate):
    qc = QuantumCircuit(3)
    qc.x(0)
    qc.barrier()
    qc.cx(0, 1)
    qc.h([0, 1])
    qc.z(1)
    qc.barrier()
    qc.barrier()
    qc.tdg(0)

    circuits = candidate(qc)
    assert len(circuits) == 4
    for circuit, expected_length in zip(circuits, [1, 4, 0, 1]):
        assert len(circuit.data) == expected_length
