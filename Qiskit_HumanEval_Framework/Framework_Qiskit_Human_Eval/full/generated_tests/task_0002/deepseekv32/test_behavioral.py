# BEHAVIORAL tests — Qiskit HumanEval task task_0002
# Generated: 2026-04-28T11:20:18.215906
# Model: deepseek/deepseek-v3.2 (deepseekv32)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    solution = (Statevector.from_label("00") + Statevector.from_label("11")) / sqrt(2)\n    assert result.equiv(solution)\n'
ENTRY_POINT_NAME = 'create_bell_statevector'
# --- Official check block end ---
import numpy as np

def test_bell_state_1():
    """Test that the returned statevector has correct shape and type."""
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    from qiskit.quantum_info import Statevector
    sv = candidate()
    assert isinstance(sv, Statevector), f"Returned object is {type(sv)}, not Statevector"
    assert sv.dim == 4, f"Statevector dimension is {sv.dim}, expected 4"
    assert sv.num_qubits == 2, f"Number of qubits is {sv.num_qubits}, expected 2"

def test_bell_state_2():
    """Test that the amplitudes match |phi+> = (|00> + |11>)/sqrt(2)."""
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    from qiskit.quantum_info import Statevector
    sv = candidate()
    data = sv.data
    expected = np.array([1.0, 0.0, 0.0, 1.0]) / np.sqrt(2)
    assert np.allclose(data, expected, atol=1e-10), f"Amplitudes {data} do not match expected {expected}"

def test_bell_state_3():
    """Test that measuring both qubits yields equal probability for 00 and 11."""
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    from qiskit.quantum_info import Statevector
    from qiskit import QuantumCircuit
    sv = candidate()
    # Build a circuit that prepares the state and measures both qubits
    qc = QuantumCircuit(2, 2)
    # The candidate returns a statevector; we can sample from it directly
    counts = sv.sample_counts(shots=2000, seed=42)
    assert len(counts) == 2, f"Expected exactly 2 outcomes, got {len(counts)}"
    prob_00 = counts.get('00', 0) / 2000
    prob_11 = counts.get('11', 0) / 2000
    assert np.isclose(prob_00, 0.5, atol=0.05), f"Probability for 00 is {prob_00}, expected ~0.5"
    assert np.isclose(prob_11, 0.5, atol=0.05), f"Probability for 11 is {prob_11}, expected ~0.5"
    # Ensure other outcomes are negligible
    prob_other = (counts.get('01', 0) + counts.get('10', 0)) / 2000
    assert prob_other < 0.01, f"Unexpected outcomes 01/10 have probability {prob_other}"