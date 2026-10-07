# BEHAVIORAL tests — Qiskit HumanEval task task_0002
# Generated: 2026-04-28T11:41:06.110588
# Model: google/gemini-3.1-pro-preview (gemini3pro)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    solution = (Statevector.from_label("00") + Statevector.from_label("11")) / sqrt(2)\n    assert result.equiv(solution)\n'
ENTRY_POINT_NAME = 'create_bell_statevector'
# --- Official check block end ---
def test_bell_statevector_type_and_dims_1():
    import builtins as _b
    from qiskit.quantum_info import Statevector
    
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    result = candidate()
    
    assert isinstance(result, Statevector), "The returned object must be a qiskit.quantum_info.Statevector."
    assert getattr(result, "num_qubits", None) == 2, f"The statevector must be for exactly 2 qubits."
    assert getattr(result, "dim", None) == 4, f"The statevector dimension must be 4."

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
    assert isinstance(result, Statevector), "Expected Statevector return type."
    
    probs = result.probabilities()
    expected_probs = np.array([0.5, 0.0, 0.0, 0.5])
    
    assert np.allclose(probs, expected_probs, atol=1e-4), (
        f"Probabilities are incorrect. Expected {expected_probs}, got {probs}."
    )

def test_bell_statevector_phase_and_fidelity_3():
    import builtins as _b
    import numpy as np
    from qiskit.quantum_info import state_fidelity, Statevector
    
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    result = candidate()
    assert isinstance(result, Statevector), "Expected Statevector return type."
    
    expected = Statevector(np.array([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)]))
    
    fid = state_fidelity(result, expected)
    
    assert np.isclose(fid, 1.0, atol=1e-4), (
        f"The state fidelity with the ideal Phi+ state is {fid}, but should be 1.0. "
        "Make sure the relative phase between |00> and |11> is correct."
    )