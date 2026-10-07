# BEHAVIORAL tests — Qiskit HumanEval task task_0002
# Generated: 2026-04-28T12:34:00.893833
# Model: openai/gpt-5.4 (gpt54)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    solution = (Statevector.from_label("00") + Statevector.from_label("11")) / sqrt(2)\n    assert result.equiv(solution)\n'
ENTRY_POINT_NAME = 'create_bell_statevector'
# --- Official check block end ---
def test_bell_statevector_amplitudes_1():
    import builtins as _b
    import numpy as np
    from math import sqrt
    from qiskit.quantum_info import Statevector

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    result = candidate()

    assert isinstance(result, Statevector), "create_bell_statevector must return a qiskit.quantum_info.Statevector instance."
    data = np.asarray(result.data, dtype=complex)
    expected = np.array([1 / sqrt(2), 0, 0, 1 / sqrt(2)], dtype=complex)

    assert data.shape == (4,), "Returned statevector must represent a 2-qubit state with 4 amplitudes."
    assert np.allclose(data, expected, atol=1e-4, rtol=1e-5), "Returned statevector amplitudes must match the phi+ Bell state (|00> + |11>)/sqrt(2)."


def test_bell_statevector_probabilities_2():
    import builtins as _b
    import numpy as np

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    result = candidate()
    probs = result.probabilities_dict()

    assert set(probs.keys()).issubset({"00", "01", "10", "11"}), "Probability dictionary must correspond to a 2-qubit computational basis."
    assert np.allclose(sum(probs.values()), 1.0, atol=1e-4, rtol=1e-5), "Statevector probabilities must sum to 1."
    assert np.allclose(probs.get("00", 0.0), 0.5, atol=1e-4, rtol=1e-5), "Phi+ Bell state must have probability 0.5 on outcome '00'."
    assert np.allclose(probs.get("11", 0.0), 0.5, atol=1e-4, rtol=1e-5), "Phi+ Bell state must have probability 0.5 on outcome '11'."
    assert np.allclose(probs.get("01", 0.0), 0.0, atol=1e-4, rtol=1e-5), "Phi+ Bell state must have zero probability on outcome '01'."
    assert np.allclose(probs.get("10", 0.0), 0.0, atol=1e-4, rtol=1e-5), "Phi+ Bell state must have zero probability on outcome '10'."


def test_bell_statevector_entanglement_and_phase_3():
    import builtins as _b
    import numpy as np
    from qiskit.quantum_info import Statevector, partial_trace

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    result = candidate()

    assert isinstance(result, Statevector), "Function must return a Statevector object."
    rho_reduced = partial_trace(result, [1])
    expected_reduced = np.array([[0.5, 0.0], [0.0, 0.5]], dtype=complex)

    assert np.allclose(rho_reduced.data, expected_reduced, atol=1e-4, rtol=1e-5), "A phi+ Bell state must be entangled, giving a maximally mixed one-qubit reduced state."

    data = np.asarray(result.data, dtype=complex)
    assert np.allclose(data[1], 0.0, atol=1e-4, rtol=1e-5) and np.allclose(data[2], 0.0, atol=1e-4, rtol=1e-5), "Phi+ Bell state must have no amplitude on |01> or |10>."
    assert np.allclose(data[0], data[3], atol=1e-4, rtol=1e-5), "Phi+ Bell state requires equal-phase amplitudes on |00> and |11>, not opposite-sign or different-phase amplitudes."