import numpy as np
from typing import Union
from qiskit_ibm_runtime.fake_provider.fake_backend import FakeBackendV2
from qiskit_ibm_runtime import IBMBackend
def qubit_with_least_readout_error(backend: Union[IBMBackend, FakeBackendV2])-> float:
    """ Return the minimum readout error of any input backend of type FakeBackendV2, IBMBackend.
    """

    error_list = []
    if issubclass(type(backend), FakeBackendV2):    
        for qubits in range(backend.num_qubits):
            error_list.append(backend.target["measure"][(qubits,)].error)
    else:
        for qubits in range(backend.configuration().num_qubits):
            error_list.append(backend.properties().readout_error(qubits))
    return np.min(error_list)
