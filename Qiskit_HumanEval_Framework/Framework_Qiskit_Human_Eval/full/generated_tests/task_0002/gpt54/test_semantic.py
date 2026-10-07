# SEMANTIC tests — Qiskit HumanEval task task_0002
# Generated: 2026-04-28T12:33:47.844246
# Model: openai/gpt-5.4 (gpt54)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    solution = (Statevector.from_label("00") + Statevector.from_label("11")) / sqrt(2)\n    assert result.equiv(solution)\n'
ENTRY_POINT_NAME = 'create_bell_statevector'
# --- Official check block end ---
def test_bell_statevector_type_and_amplitudes_1():
    import builtins as _b
    import numpy as np
    from qiskit.quantum_info import Statevector
    from math import sqrt

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    result = candidate()

    assert isinstance(result, Statevector), "create_bell_statevector should return a qiskit.quantum_info.Statevector instance."

    expected = np.array([1 / sqrt(2), 0, 0, 1 / sqrt(2)], dtype=complex)
    actual = np.asarray(result.data, dtype=complex)

    assert actual.shape == (4,), "Returned Statevector should represent a 2-qubit state with 4 amplitudes."
    assert np.allclose(actual, expected, atol=1e-4, rtol=1e-5), "Returned statevector should be the phi+ Bell state |00>+|11> over sqrt(2)."


def test_bell_statevector_probabilities_and_entanglement_2():
    import builtins as _b
    import numpy as np

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    sv = candidate()
    probs = sv.probabilities()

    expected_probs = np.array([0.5, 0.0, 0.0, 0.5], dtype=float)
    assert probs.shape == (4,), "Bell state probabilities should have length 4 for a 2-qubit system."
    assert np.allclose(probs, expected_probs, atol=1e-4, rtol=1e-5), "Phi+ Bell state should have probability 1/2 on |00> and |11>, and 0 on |01>, |10>."

    reduced_0 = sv.partial_trace([1]).data
    reduced_1 = sv.partial_trace([0]).data
    expected_reduced = 0.5 * np.eye(2, dtype=complex)

    assert np.allclose(reduced_0, expected_reduced, atol=1e-4, rtol=1e-5), "Tracing out one qubit of a Bell state should give the maximally mixed single-qubit state."
    assert np.allclose(reduced_1, expected_reduced, atol=1e-4, rtol=1e-5), "Either qubit of the Bell state should have maximally mixed reduced density matrix."


def test_bell_statevector_correlations_3():
    import builtins as _b
    import numpy as np
    from qiskit.quantum_info import SparsePauliOp
    from math import sqrt

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    sv = candidate()

    zz = SparsePauliOp.from_list([("ZZ", 1.0)])
    xx = SparsePauliOp.from_list([("XX", 1.0)])
    yy = SparsePauliOp.from_list([("YY", 1.0)])

    exp_zz = sv.expectation_value(zz)
    exp_xx = sv.expectation_value(xx)
    exp_yy = sv.expectation_value(yy)

    assert np.allclose(exp_zz, 1.0, atol=1e-4, rtol=1e-5), "Phi+ Bell state should have +1 expectation value for ZZ."
    assert np.allclose(exp_xx, 1.0, atol=1e-4, rtol=1e-5), "Phi+ Bell state should have +1 expectation value for XX."
    assert np.allclose(exp_yy, -1.0, atol=1e-4, rtol=1e-5), "Phi+ Bell state should have -1 expectation value for YY."