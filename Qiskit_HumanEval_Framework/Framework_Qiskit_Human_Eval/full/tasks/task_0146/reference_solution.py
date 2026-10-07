from qiskit.transpiler import PassManager, StagedPassManager
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.transpiler.passes.layout.trivial_layout import TrivialLayout
def trivial_layout() -> StagedPassManager:
    """ Generate Qiskit code that sets up a StagedPassManager with a trivial layout using PassManager for the least busy backend available.
    """

    pm_opt = StagedPassManager()
    pm_opt.layout = PassManager()
    backend = QiskitRuntimeService().least_busy()
    cm = backend.coupling_map
    pm_opt.layout += TrivialLayout(cm)
    return pm_opt
