from qiskit_ibm_runtime import fake_provider
import inspect
def backend_info(backend_name):
    """ Given the fake backend name, retrieve information about the backend's number of qubits, coupling map, and supported instructions using the Qiskit Runtime Fake Provider, 
    and create a dictionary containing the info. The dictionary must have the following keys: 'num_qubits' (the number of qubits), 'coupling_map' 
    (the coupling map of the backend), and 'supported_instructions' (the supported instructions of the backend).
    """

    # Find the backend class by searching through all fake backends
    backend_class = None
    for name, obj in inspect.getmembers(fake_provider):
        if inspect.isclass(obj) and name.startswith('Fake'):
            try:
                temp_backend = obj()
                if temp_backend.name == backend_name:
                    backend_class = obj
                    break
            except:
                pass
    
    if backend_class is None:
        raise ValueError(f"Backend '{backend_name}' not found")
    
    backend = backend_class()
    config = backend.configuration()
    dict_result = {"num_qubits": config.num_qubits, "coupling_map": config.coupling_map, "supported_instructions": config.supported_instructions}

    return dict_result
