from qiskit.circuit import QuantumCircuit
from qiskit_ibm_runtime.fake_provider import FakeKyoto, FakeKyiv, FakeAuckland
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
def backend_with_least_instructions() -> str:
    """ Transpile the circuit for the phi plus bell state for FakeKyoto, FakeKyiv and FakeAuckland using the level 0 preset pass manager and return the backend name with the lowest number of instructions.
    """

    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    backends = [FakeKyiv(), FakeKyoto(), FakeAuckland()]
    qc_isa_num_intruc = {}
    for backend in backends:
        pm = generate_preset_pass_manager(optimization_level=0, backend=backend)
        qc_isa_num_intruc[backend.name] = len(pm.run(qc).data)
    return min(qc_isa_num_intruc, key=qc_isa_num_intruc.get)
