# SEMANTIC tests — Qiskit HumanEval task task_0063
# Generated: 2026-04-28T12:38:26.261725
# Model: openai/gpt-5.4 (gpt54)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from numpy.random import seed\n    seed(12345)\n    basis = [1, 0, 0, 1, 1]\n    circuit = QuantumCircuit(5)\n    circuit.x([3, 4])\n    circuit.h([0, 3, 4])\n    result = candidate(basis, circuit)\n    assert result == "1"\n'
ENTRY_POINT_NAME = 'bb84_circuit_generate_key'
# --- Official check block end ---
def test_key_generation_matching_z_basis_1():
    import builtins as _b
    import numpy as np
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    senders_basis = [0, 0, 0]
    qc = QuantumCircuit(3, 3)
    qc.x(0)
    qc.x(2)

    pre_sv = Statevector.from_instruction(qc)
    key = candidate(senders_basis, qc)

    assert isinstance(key, str), "The generated key must be returned as a string."
    assert key == "101", "For a circuit preparing |101> in Z basis, the generated BB84 key should be '101'."

    post_sv = Statevector.from_instruction(qc.remove_final_measurements(inplace=False))
    assert np.allclose(pre_sv.data, post_sv.data, atol=1e-4, rtol=1e-5), "Key generation should not change the prepared quantum state apart from adding final measurements."
    assert qc.num_clbits >= 3, "The circuit should have enough classical bits to measure all qubits when generating the key."
    assert any(inst.operation.name == "measure" for inst in qc.data), "The circuit should include measurement operations after key generation."


def test_key_generation_with_x_basis_states_2():
    import builtins as _b
    import numpy as np
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    senders_basis = [1, 1, 1]
    qc = QuantumCircuit(3, 3)
    qc.h(0)
    qc.x(1)
    qc.h(1)
    qc.h(2)

    pre_sv = Statevector.from_instruction(qc)
    key = candidate(senders_basis, qc)

    assert isinstance(key, str), "The generated key must be a string for X-basis inputs as well."
    assert key == "101", "For states |->, |+>, |-> encoded in X basis, the generated BB84 key should be '101'."

    no_meas_circ = qc.remove_final_measurements(inplace=False)
    post_sv = Statevector.from_instruction(no_meas_circ)
    assert np.allclose(pre_sv.data, post_sv.data, atol=1e-4, rtol=1e-5), "Basis-matching key extraction should preserve the pre-measurement state and only append final operations."
    measure_count = sum(1 for inst in qc.data if inst.operation.name == "measure")
    assert measure_count == 3, "The circuit should measure each qubit exactly once for a 3-qubit BB84 key extraction."


def test_empty_basis_and_circuit_3():
    import builtins as _b
    from qiskit import QuantumCircuit

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    senders_basis = []
    qc = QuantumCircuit(0, 0)

    key = candidate(senders_basis, qc)

    assert isinstance(key, str), "Even for an empty input, the function should return a string."
    assert key == "", "For an empty sender basis and empty circuit, the generated key should be the empty string."
    assert len(qc.data) == 0, "An empty circuit should remain unchanged and should not gain operations when generating an empty key."