def check(candidate):
    unitary = random_unitary(4)
    try:
        qc = candidate(unitary)
        assert isinstance(qc, QuantumCircuit)
        assert qc.num_qubits == 2
        assert qc.size() > 0

        cx_count = sum(1 for inst in qc.data if inst.operation.name == "cx")
        assert cx_count > 0
    except (ValueError, np.linalg.LinAlgError) as e:
        raise e
