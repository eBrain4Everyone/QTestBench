def check(candidate):
    from qiskit_ibm_runtime.fake_provider import FakeKyiv
    from qiskit.circuit.random import random_circuit
    from qiskit.transpiler.passes import CheckMap
    backend = FakeKyiv()
    for _ in range(3):
        qc = random_circuit(5,5)
        original_ops = qc.count_ops()
        original_ops.pop("swap", None)

        mapped_qc = candidate(qc, backend)

        check_map = CheckMap(coupling_map=backend.coupling_map)
        dag = circuit_to_dag(mapped_qc)
        check_map.run(dag)
        assert check_map.property_set["is_swap_mapped"]

        mapped_ops = mapped_qc.count_ops()
        mapped_ops.pop("swap", None)

        # We convert to set for comparison to ignore dictionary ordering
        assert set(original_ops.items()) == set(mapped_ops.items())
