# BEHAVIORAL tests — Qiskit HumanEval task task_0002
# Generated: 2026-04-28T12:39:30.877964
# Model: qwen/qwen3-coder-next (qwen3)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    solution = (Statevector.from_label("00") + Statevector.from_label("11")) / sqrt(2)\n    assert result.equiv(solution)\n'
ENTRY_POINT_NAME = 'create_bell_statevector'
# --- Official check block end ---
import numpy as np

def test_bell_statevector_correct_form_1():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    from qiskit.quantum_info import Statevector
    
    state = candidate()
    assert isinstance(state, Statevector), "Function should return a Statevector object"
    
    # Expected phi+ Bell state: [1/sqrt(2), 0, 0, 1/sqrt(2)]
    expected = Statevector.from_label('00').data * (1/np.sqrt(2)) + Statevector.from_label('11').data * (1/np.sqrt(2))
    
    # Check numerical closeness
    assert np.allclose(state.data, expected.data, atol=1e-7), f"Statevector does not match expected phi+ Bell state. Got {state.data}, expected {expected.data}"


def test_bell_statevector_normalized_2():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    state = candidate()
    # Check normalization: sum of squared amplitudes should be 1
    norm_squared = sum(np.abs(state.data)**2)
    assert np.isclose(norm_squared, 1.0, atol=1e-7), f"Statevector not normalized. Norm squared = {norm_squared}"


def test_bell_statevector_measurements_3():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector
    
    state = candidate()
    
    # Simulate measurement in computational basis by checking probabilities
    probs = np.abs(state.data)**2
    # Expected: |00> and |11> each with 50% probability, others 0%
    expected_probs = np.array([0.5, 0.0, 0.0, 0.5])
    
    assert np.allclose(probs, expected_probs, atol=1e-7), f"Measurement probabilities incorrect. Got {probs}, expected {expected_probs}"