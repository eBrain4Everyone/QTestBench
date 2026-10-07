def check(candidate):
    from qiskit_ibm_runtime.fake_provider import FakeKyoto
    from qiskit_ibm_runtime import QiskitRuntimeService
    backend_v2 = FakeKyoto()
    error_can_v2 = candidate(backend_v2)
    error_list_v2 = []
    for qubits in range(backend_v2.num_qubits):
        error_list_v2.append(backend_v2.target["measure"][(qubits,)].error)
    error_exp_v2 = np.min(error_list_v2)
    assert error_can_v2 == error_exp_v2, "The qubit returned doesn't have the least readout error"
    backend_ser = QiskitRuntimeService().least_busy()
    error_can_ser = candidate(backend_ser)
    error_list_ser = []
    for qubits in range(backend_ser.configuration().num_qubits):
        error_list_ser.append(backend_ser.properties().readout_error(qubits))
    error_exp_ser = np.min(error_list_ser)
    assert error_can_ser == error_exp_ser, "The qubit returned doesn't have the least readout error"
