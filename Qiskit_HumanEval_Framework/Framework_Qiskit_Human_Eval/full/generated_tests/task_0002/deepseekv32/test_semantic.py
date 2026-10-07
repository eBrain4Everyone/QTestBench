# SEMANTIC tests — Qiskit HumanEval task task_0002
# Generated: 2026-04-28T11:19:48.819687
# Model: deepseek/deepseek-v3.2 (deepseekv32)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    solution = (Statevector.from_label("00") + Statevector.from_label("11")) / sqrt(2)\n    assert result.equiv(solution)\n'
ENTRY_POINT_NAME = 'create_bell_statevector'
# --- Official check block end ---
import pytest
import numpy as np
import builtins as _b

def test_bell_statevector_1():
    """Test that the returned statevector matches the phi+ Bell state."""
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    from qiskit.quantum_info import Statevector
    sv = candidate()
    assert isinstance(sv, Statevector), f"Expected Statevector, got {type(sv)}"
    # phi+ = (|00> + |11>)/sqrt(2)
    expected = np.array([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)])
    actual = sv.data
    # compare up to global phase (allow multiplication by e^{i_})
    # normalize both to have first element real positive
    if np.abs(actual[0]) > 1e-10:
        phase = np.angle(actual[0])
        actual_adj = actual * np.exp(-1j * phase)
    else:
        actual_adj = actual
    if np.abs(expected[0]) > 1e-10:
        phase = np.angle(expected[0])
        expected_adj = expected * np.exp(-1j * phase)
    else:
        expected_adj = expected
    assert np.allclose(actual_adj, expected_adj, atol=1e-4, rtol=1e-5), f"Statevector mismatch. Expected {expected}, got {sv.data}"

def test_bell_statevector_2():
    """Test that the statevector is properly normalized."""
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    from qiskit.quantum_info import Statevector
    sv = candidate()
    norm = np.linalg.norm(sv.data)
    assert np.allclose(norm, 1.0, atol=1e-4, rtol=1e-5), f"Statevector not normalized: norm = {norm}"

def test_bell_statevector_3():
    """Test that measurements in the computational basis produce equal probabilities for |00> and |11>."""
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    from qiskit.quantum_info import Statevector
    sv = candidate()
    probs = sv.probabilities()
    expected_probs = [0.5, 0.0, 0.0, 0.5]
    assert np.allclose(probs, expected_probs, atol=1e-4, rtol=1e-5), f"Probabilities mismatch. Expected {expected_probs}, got {probs}"