# SEMANTIC tests — Qiskit HumanEval task task_0002
# Generated: 2026-04-28T12:39:25.100297
# Model: qwen/qwen3-coder-next (qwen3)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    solution = (Statevector.from_label("00") + Statevector.from_label("11")) / sqrt(2)\n    assert result.equiv(solution)\n'
ENTRY_POINT_NAME = 'create_bell_statevector'
# --- Official check block end ---
import numpy as np
import pytest

def test_bell_statevector_is_phi_plus_1():
    from qiskit.quantum_info import Statevector
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    state = candidate()
    expected = Statevector.from_label('00') + Statevector.from_label('11')
    expected = expected / np.linalg.norm(expected)
    
    # Compare up to global phase
    overlap = abs(np.vdot(state.data, expected.data))
    assert np.isclose(overlap, 1.0, atol=1e-4), f"State is not a Bell state |___: overlap = {overlap}"

def test_bell_statevector_has_correct_marginal_probabilities_2():
    from qiskit.quantum_info import Statevector
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    state = candidate()
    probs = state.probabilities()
    
    # For |___ = (|00_ + |11_)/_2, measurement in computational basis yields 00 or 11 each with prob 0.5
    expected_probs = np.array([0.5, 0.0, 0.0, 0.5])
    assert np.allclose(probs, expected_probs, atol=1e-4), f"Measurement probabilities incorrect: {probs}"

def test_bell_statevector_is_entangled_3():
    from qiskit.quantum_info import Statevector, partial_trace
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    state = candidate()
    
    # Compute purity of reduced density matrix of first qubit
    rho = state.to_density_matrix()
    rho_A = partial_trace(rho, [1])  # trace out second qubit
    purity = np.real(np.trace(rho_A @ rho_A))
    
    # For maximally entangled Bell state, purity of reduced state = 0.5
    assert np.isclose(purity, 0.5, atol=1e-4), f"State is not entangled: reduced qubit purity = {purity}"