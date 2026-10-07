from qiskit_ibm_runtime.fake_provider import FakeOsaka, FakeSherbrooke, FakeBrisbane
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.synthesis.qft import synth_qft_full
def backend_with_highest_complexity():
    """ Transpile the 4-qubit QFT circuit using preset passmanager with optimization level 3 and seed transpiler = 1234 in FakeOsaka, FakeSherbrooke and FakeBrisbane. Compute the cost of the instructions by penalizing the two qubit gate with a cost of 5, rz gates with a cost 1 and other gates with a cost 2 and return the value of the highest cost among these backends.
    """

    qc = synth_qft_full(4)
    backends = [FakeOsaka(), FakeSherbrooke(), FakeBrisbane()]
    complexity_dict = {}
    for backend in backends:
        pm = generate_preset_pass_manager(
            optimization_level=3, seed_transpiler=1234, backend=backend
        )
        data = pm.run(qc).data
        complexity = 0
        for instruc in data:
            if instruc.operation.num_qubits == 2:
                complexity += 5
            elif instruc.operation.name == "rz":
                complexity += 1
            else:
                complexity += 2
        complexity_dict[backend.name] = complexity
    return complexity_dict[max(complexity_dict, key=complexity_dict.get)]
