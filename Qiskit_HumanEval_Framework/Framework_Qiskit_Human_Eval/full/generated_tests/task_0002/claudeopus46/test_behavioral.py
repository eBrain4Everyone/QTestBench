# BEHAVIORAL tests — Qiskit HumanEval task task_0002
# Generated: 2026-04-28T11:10:12.994106
# Model: anthropic/claude-opus-4-6 (claudeopus46)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    solution = (Statevector.from_label("00") + Statevector.from_label("11")) / sqrt(2)\n    assert result.equiv(solution)\n'
ENTRY_POINT_NAME = 'create_bell_statevector'
# --- Official check block end ---
def test_bell_statevector_type_1():
    import builtins as _b
    from qiskit.quantum_info import Statevector
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    result = candidate()
    assert isinstance(result, Statevector), (
        f"Expected return type Statevector, got {type(result)}"
    )
    assert result.num_qubits == 2, (
        f"Expected 2-qubit statevector, got {result.num_qubits} qubits"
    )


def test_bell_statevector_probabilities_2():
    import builtins as _b
    import numpy as np
    from qiskit.quantum_info import Statevector
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    result = candidate()
    probs = result.probabilities_dict()
    
    # phi+ = (|00> + |11>) / sqrt(2)
    # Should have ~0.5 probability for |00> and |11>, 0 for |01> and |10>
    p00 = probs.get("00", 0.0)
    p11 = probs.get("11", 0.0)
    p01 = probs.get("01", 0.0)
    p10 = probs.get("10", 0.0)
    
    assert np.isclose(p00, 0.5, atol=1e-6), (
        f"Probability of |00> should be 0.5, got {p00}"
    )
    assert np.isclose(p11, 0.5, atol=1e-6), (
        f"Probability of |11> should be 0.5, got {p11}"
    )
    assert np.isclose(p01, 0.0, atol=1e-6), (
        f"Probability of |01> should be 0.0, got {p01}"
    )
    assert np.isclose(p10, 0.0, atol=1e-6), (
        f"Probability of |10> should be 0.0, got {p10}"
    )


def test_bell_statevector_amplitudes_3():
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
    data = result.data
    
    # phi+ = (|00> + |11>) / sqrt(2)
    # In Qiskit's ordering, the statevector is [alpha_00, alpha_01, alpha_10, alpha_11]
    # So we expect [1/sqrt(2), 0, 0, 1/sqrt(2)]
    expected = np.array([1/sqrt(2), 0, 0, 1/sqrt(2)], dtype=complex)
    
    # Allow global phase difference: check if |<expected|result>| ~ 1
    overlap = abs(np.dot(np.conj(expected), data))
    assert np.isclose(overlap, 1.0, atol=1e-6), (
        f"Statevector does not match phi+ Bell state (overlap={overlap}). "
        f"Got amplitudes {data}, expected {expected} up to global phase."
    )
    
    # Also verify it's a valid (normalized) statevector
    norm = np.sum(np.abs(data)**2)
    assert np.isclose(norm, 1.0, atol=1e-6), (
        f"Statevector is not normalized, norm={norm}"
    )