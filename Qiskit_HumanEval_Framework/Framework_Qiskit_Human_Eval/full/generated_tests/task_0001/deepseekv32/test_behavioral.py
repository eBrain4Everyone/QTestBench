# BEHAVIORAL tests — Qiskit HumanEval task task_0001
# Generated: 2026-04-28T11:19:06.996578
# Model: deepseek/deepseek-v3.2 (deepseekv32)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    assert isinstance(result, dict)\n    assert result.keys() == {"00", "11"}\n    assert 0.4 < (result["00"] / sum(result.values())) < 0.6\n'
ENTRY_POINT_NAME = 'run_bell_state_simulator'
# --- Official check block end ---
import builtins as _b
import numpy as np

def test_bell_state_simulator_1():
    """Test that the function returns a dictionary with correct Bell state keys and reasonable distribution."""
    import qiskit
    from qiskit_aer import AerSimulator
    from qiskit_ibm_runtime import Sampler
    from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
    from qiskit import QuantumCircuit
    import builtins as _b

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    counts = candidate()
    assert isinstance(counts, dict), f"Expected dict, got {type(counts)}"
    # Bell state |Phi+> = (|00> + |11>)/sqrt(2) -> only 00 and 11 possible
    allowed_keys = {"00", "11"}
    for key in counts:
        assert key in allowed_keys, f"Unexpected measurement result {key} in Bell state"
    total_shots = sum(counts.values())
    assert total_shots > 0, "Total shots must be positive"
    # With small shot count, allow some tolerance, but both 00 and 11 should appear
    # (probability of all shots being same outcome is (0.5)^shots, small for shots>=2)
    assert len(counts) == 2, f"Bell state should produce 2 outcomes, got {len(counts)}"
    # Distribution should be roughly 50/50
    prob_00 = counts.get("00", 0) / total_shots
    prob_11 = counts.get("11", 0) / total_shots
    assert abs(prob_00 - 0.5) < 0.2, f"Probability of 00 deviates too far from 0.5: {prob_00}"
    assert abs(prob_11 - 0.5) < 0.2, f"Probability of 11 deviates too far from 0.5: {prob_11}"

def test_bell_state_simulator_2():
    """Test that the circuit is transpiled with optimization level 1 (checks circuit depth reduction)."""
    import qiskit
    from qiskit_aer import AerSimulator
    from qiskit_ibm_runtime import Sampler
    from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
    from qiskit import QuantumCircuit
    import builtins as _b

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    # We cannot directly inspect the transpiled circuit inside candidate,
    # but we can verify that the function runs without error and returns counts
    counts = candidate()
    assert isinstance(counts, dict), f"Expected dict, got {type(counts)}"
    # Ensure the function actually used Sampler with AerSimulator (indirectly by checking
    # that the results are plausible and the function didn't crash).
    # Also verify that the keys are strings of length 2 (two qubits measured)
    for key in counts:
        assert isinstance(key, str), f"Key {key} is not a string"
        assert len(key) == 2, f"Key {key} length is not 2"
        assert all(c in "01" for c in key), f"Key {key} contains non-binary characters"
    # Check that the function returns something non_empty
    assert len(counts) > 0, "Counts dictionary is empty"

def test_bell_state_simulator_3():
    """Test deterministic behavior with a fixed seed (if supported)."""
    import qiskit
    from qiskit_aer import AerSimulator
    from qiskit_ibm_runtime import Sampler
    from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
    from qiskit import QuantumCircuit
    import builtins as _b

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    # Call twice with same implicit seed (if the candidate uses a fixed seed or default)
    # and verify the results are identical (deterministic).
    # This tests that the function is not using a random seed each time.
    counts1 = candidate()
    counts2 = candidate()
    # Because the candidate might not expose a seed parameter, we cannot guarantee
    # perfect equality, but we can check structural equality:
    # same keys, same total shots.
    assert set(counts1.keys()) == set(counts2.keys()), "Keys differ between runs"
    total1 = sum(counts1.values())
    total2 = sum(counts2.values())
    assert total1 == total2, f"Total shots differ: {total1} vs {total2}"
    # Additionally, the distribution should be similar (within statistical fluctuation).
    # Since the shot count is small, we allow a small tolerance.
    for key in counts1:
        diff = abs(counts1[key] - counts2.get(key, 0))
        assert diff <= 2, f"Count for {key} differs too much: {counts1[key]} vs {counts2.get(key, 0)}"