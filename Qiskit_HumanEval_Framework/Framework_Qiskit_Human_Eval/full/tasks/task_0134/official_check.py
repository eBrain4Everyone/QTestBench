def check(candidate):
    result = candidate()
    assert isinstance(result, list)
    
    service = QiskitRuntimeService()
    backends = service.backends(simulator=False, operational=True, min_num_qubits=20)
    backend_info = []
    for b in backends:
        backend_info.append({"backend_name": b.name, "num_qubits": b.num_qubits, "instructions": b.operation_names})        
    sorted_backend_info_expected = sorted(backend_info, key=lambda x: x["backend_name"])
    assert sorted_backend_info_expected == result
