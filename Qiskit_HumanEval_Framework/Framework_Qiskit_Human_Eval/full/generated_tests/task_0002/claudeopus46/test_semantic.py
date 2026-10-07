# SEMANTIC tests — Qiskit HumanEval task task_0002
# Generated: 2026-04-28T11:09:58.713562
# Model: anthropic/claude-opus-4-6 (claudeopus46)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    solution = (Statevector.from_label("00") + Statevector.from_label("11")) / sqrt(2)\n    assert result.equiv(solution)\n'
ENTRY_POINT_NAME = 'create_bell_statevector'
# --- Official check block end ---
import pytest

def test_bell_statevector_type_1():
    import builtins as _b
    import numpy as np
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    from qiskit.quantum_info import Statevector

    result = candidate()
    assert isinstance(result, Statevector), (
        f"Expected return type Statevector, got {type(result)}"
    )
    assert result.num_qubits == 2, (
        f"Expected a 2-qubit statevector, got {result.num_qubits} qubits"
    )


def test_bell_statevector_amplitudes_2():
    import builtins as _b
    import numpy as np
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    from qiskit.quantum_info import Statevector
    from math import sqrt

    result = candidate()
    data = np.array(result.data)

    # phi+ = (|00> + |11>) / sqrt(2)
    expected = np.array([1 / sqrt(2), 0, 0, 1 / sqrt(2)])

    # Compare up to global phase: |<expected|result>| should be ~1
    overlap = np.abs(np.dot(np.conj(expected), data))
    assert np.isclose(overlap, 1.0, atol=1e-4, rtol=1e-5), (
        f"Statevector does not match phi+ Bell state. "
        f"Overlap with expected state: {overlap}. "
        f"Got amplitudes: {data}"
    )


def test_bell_statevector_probabilities_3():
    import builtins as _b
    import numpy as np
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    result = candidate()
    probs = result.probabilities()

    # phi+ has probability 0.5 for |00> and 0.5 for |11>, 0 for |01> and |10>
    expected_probs = np.array([0.5, 0.0, 0.0, 0.5])
    assert np.allclose(probs, expected_probs, atol=1e-4, rtol=1e-5), (
        f"Probabilities do not match phi+ Bell state. "
        f"Expected {expected_probs}, got {probs}"
    )

    # Verify the state is valid (normalized)
    assert np.isclose(np.sum(probs), 1.0, atol=1e-6), (
        f"Statevector is not normalized. Probabilities sum to {np.sum(probs)}"
    )

    # Verify it's entangled by checking partial trace purity
    from qiskit.quantum_info import partial_trace
    rho_reduced = partial_trace(result, [1])
    purity = np.real(np.trace(rho_reduced.data @ rho_reduced.data))
    assert np.isclose(purity, 0.5, atol=1e-4), (
        f"State does not appear maximally entangled. "
        f"Reduced state purity: {purity}, expected 0.5"
    )