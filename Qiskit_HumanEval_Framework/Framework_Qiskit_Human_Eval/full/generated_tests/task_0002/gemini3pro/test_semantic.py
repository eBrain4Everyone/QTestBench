# SEMANTIC tests — Qiskit HumanEval task task_0002
# Generated: 2026-04-28T11:40:45.086320
# Model: google/gemini-3.1-pro-preview (gemini3pro)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    solution = (Statevector.from_label("00") + Statevector.from_label("11")) / sqrt(2)\n    assert result.equiv(solution)\n'
ENTRY_POINT_NAME = 'create_bell_statevector'
# --- Official check block end ---
import builtins as _b

def test_bell_statevector_type_and_dims_1():
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    from qiskit.quantum_info import Statevector
    import numpy as np
    
    result = candidate()
    assert isinstance(result, Statevector), "Return type must be an instance of qiskit.quantum_info.Statevector"
    assert result.num_qubits == 2, f"Expected 2 qubits, got {result.num_qubits}"
    
    norm = np.linalg.norm(result.data)
    assert np.isclose(norm, 1.0, atol=1e-4, rtol=1e-5), f"Statevector should be normalized, got norm {norm}"

def test_bell_statevector_fidelity_2():
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    from qiskit.quantum_info import Statevector, state_fidelity
    import numpy as np
    
    result = candidate()
    expected_sv = Statevector([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)])
    fid = state_fidelity(result, expected_sv)
    
    assert np.isclose(fid, 1.0, atol=1e-4, rtol=1e-5), f"Expected fidelity 1.0 with phi+ state, got {fid}"

def test_bell_statevector_amplitudes_3():
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    import numpy as np
    
    result = candidate()
    data = result.data
    
    assert np.allclose(data[1], 0, atol=1e-4), f"Amplitude of |01> must be 0, got {data[1]}"
    assert np.allclose(data[2], 0, atol=1e-4), f"Amplitude of |10> must be 0, got {data[2]}"
    
    mag_00 = np.abs(data[0])
    mag_11 = np.abs(data[3])
    
    assert np.isclose(mag_00, 1/np.sqrt(2), atol=1e-4), f"Magnitude of |00> should be ~0.707, got {mag_00}"
    assert np.isclose(mag_11, 1/np.sqrt(2), atol=1e-4), f"Magnitude of |11> should be ~0.707, got {mag_11}"
    
    # Check relative phase
    angle_00 = np.angle(data[0])
    angle_11 = np.angle(data[3])
    phase_diff = (angle_00 - angle_11) % (2 * np.pi)
    
    phase_valid = np.isclose(phase_diff, 0, atol=1e-4) or np.isclose(phase_diff, 2*np.pi, atol=1e-4)
    assert phase_valid, f"Relative phase between |00> and |11> must be 0, got {phase_diff}"