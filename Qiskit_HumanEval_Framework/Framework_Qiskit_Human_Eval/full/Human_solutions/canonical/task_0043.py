from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.transpiler.passmanager import StagedPassManager
from qiskit_ibm_runtime import QiskitRuntimeService
def generate_pass_manager_obj()-> StagedPassManager:
    """ Instantiate a preset_passmanager using Qiskit using the least busy device available and optimization level 3. Return the resulting passmanager instance.
    """

    provider = QiskitRuntimeService()
    backend = provider.least_busy()
    pass_manager = generate_preset_pass_manager(optimization_level=3, backend=backend)
    return pass_manager
