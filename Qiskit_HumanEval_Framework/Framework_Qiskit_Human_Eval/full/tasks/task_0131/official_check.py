from qiskit_ibm_runtime.fake_provider import FakeCairoV2
def check(candidate):
    backend = FakeCairoV2()
    binfo_dict = candidate(backend.name)
    backend_config = backend.configuration()
    assert isinstance(binfo_dict, dict)
    assert binfo_dict["num_qubits"] == backend_config.num_qubits
    assert binfo_dict["coupling_map"] == backend_config.coupling_map
    assert binfo_dict["supported_instructions"] == backend_config.supported_instructions
