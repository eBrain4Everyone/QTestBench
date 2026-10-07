def check(candidate):
    service = QiskitRuntimeService(channel="ibm_quantum")
    backend = service.least_busy(filters=lambda b : ("rz" in b.basis_gates))
    max_rz_error_pair, max_rz_error_rate = candidate(backend.name)
    
    assert isinstance(max_rz_error_pair, (tuple, list))
    assert len(max_rz_error_pair) == 1
    assert all(isinstance(qubit, int) for qubit in max_rz_error_pair)
    assert max_rz_error_rate >= 0 and max_rz_error_rate <= 1

    backend_properties = backend.properties()
    rz_props = backend_properties.gate_property("rz")
    expected_max_rz_error_pair = max(rz_props, key=lambda x: rz_props[x]["gate_error"][0])
    expected_max_rz_error_rate = rz_props[expected_max_rz_error_pair]["gate_error"][0]
    assert (expected_max_rz_error_pair, expected_max_rz_error_rate) == (max_rz_error_pair, max_rz_error_rate)
