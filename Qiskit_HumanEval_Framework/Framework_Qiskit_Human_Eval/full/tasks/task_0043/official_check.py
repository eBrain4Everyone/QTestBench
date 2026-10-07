def check(candidate):
    from qiskit.transpiler.passmanager import StagedPassManager
    result = candidate()
    assert(type(result) == StagedPassManager)
