def check(candidate):
    from qiskit_ibm_runtime.fake_provider import FakeKyoto
    from qiskit_ibm_runtime import QiskitRuntimeService
    backend_v2 = FakeKyoto()
    backend_ser = QiskitRuntimeService().least_busy()
    connections_can_v2 = candidate(backend_v2)
    connections_exp_v2 = backend_v2.coupling_map
    assert connections_exp_v2 == connections_can_v2, "The list of connections doesn't match the two qubit connections from the backend"
    connections_can_ser = candidate(backend_ser)
    connections_exp_ser = backend_ser.configuration().coupling_map
    assert connections_exp_ser == connections_can_ser, "The list of connections doesn't match the two qubit connections from the backend"
