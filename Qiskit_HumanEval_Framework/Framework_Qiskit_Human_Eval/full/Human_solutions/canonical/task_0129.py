from qiskit_ibm_runtime import QiskitRuntimeService
def find_highest_rz_error_rate(backend_name):
    """ Given the name of a quantum backend, retrieve the properties of the specified backend and identify the qubit pair with the highest error rate among its RZ gates. 
    Return this qubit pair along with the corresponding error rate as a tuple. If the backend doesn't support the RZ gate, return None.
    """

    service = QiskitRuntimeService(channel="ibm_quantum")
    backend = service.backend(backend_name)
    backend_properties = backend.properties()

    try:
        rz_props = backend_properties.gate_property("rz")
    except:
        return None

    qubit_pair = max(rz_props, key=lambda x: rz_props[x]["gate_error"][0])
    max_rz_error = rz_props[qubit_pair]["gate_error"][0]
    return (qubit_pair, max_rz_error)
