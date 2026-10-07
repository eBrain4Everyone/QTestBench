# BEHAVIORAL tests — Qiskit HumanEval task task_0001
# Generated: 2026-04-28T12:27:36.979466
# Model: openai/gpt-5.4 (gpt54)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    assert isinstance(result, dict)\n    assert result.keys() == {"00", "11"}\n    assert 0.4 < (result["00"] / sum(result.values())) < 0.6\n'
ENTRY_POINT_NAME = 'run_bell_state_simulator'
# --- Official check block end ---
def test_bell_counts_distribution_1():
    import builtins as _b
    import numpy as np
    from unittest.mock import patch
    from qiskit.primitives import StatevectorSampler

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    class PatchedSampler:
        def __init__(self, mode=None, *args, **kwargs):
            self._sampler = StatevectorSampler(seed=123)

        def run(self, pubs, *args, **kwargs):
            if "shots" not in kwargs:
                kwargs["shots"] = 512
            return self._sampler.run(pubs, *args, **kwargs)

    with patch.dict(candidate.__globals__, {"Sampler": PatchedSampler}):
        counts = candidate()

    assert isinstance(counts, dict), "Function must return a counts dictionary."
    assert counts, "Counts dictionary must not be empty."
    keys = set(counts.keys())
    assert keys <= {"00", "11"}, f"Bell phi-plus measurement outcomes must only be '00' or '11', got {keys}."
    total = sum(counts.values())
    assert total > 0, "Total number of counts must be positive."
    p00 = counts.get("00", 0) / total
    p11 = counts.get("11", 0) / total
    assert np.allclose(p00 + p11, 1.0, atol=1e-4, rtol=1e-5), "Probabilities for '00' and '11' should sum to 1."
    assert 0.35 <= p00 <= 0.65, f"Outcome '00' should occur about half the time for phi-plus, got proportion {p00}."
    assert 0.35 <= p11 <= 0.65, f"Outcome '11' should occur about half the time for phi-plus, got proportion {p11}."


def test_output_is_integer_counts_and_no_forbidden_states_2():
    import builtins as _b
    from unittest.mock import patch
    from qiskit.primitives import StatevectorSampler

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    class PatchedSampler:
        def __init__(self, mode=None, *args, **kwargs):
            self._sampler = StatevectorSampler(seed=321)

        def run(self, pubs, *args, **kwargs):
            if "shots" not in kwargs:
                kwargs["shots"] = 256
            return self._sampler.run(pubs, *args, **kwargs)

    with patch.dict(candidate.__globals__, {"Sampler": PatchedSampler}):
        counts = candidate()

    assert isinstance(counts, dict), "Returned value must be a dictionary of measurement counts."
    for bitstring, value in counts.items():
        assert isinstance(bitstring, str), f"Count keys must be bitstrings, got key of type {type(bitstring)}."
        assert len(bitstring) == 2, f"Bell-state experiment should produce 2-bit outcomes, got key {bitstring!r}."
        assert set(bitstring) <= {"0", "1"}, f"Bitstring keys must contain only '0' and '1', got {bitstring!r}."
        assert isinstance(value, int), f"Count values must be integers, got {type(value)} for key {bitstring!r}."
        assert value >= 0, f"Count values must be nonnegative, got {value} for key {bitstring!r}."

    assert counts.get("01", 0) == 0, f"State '01' should not appear for a phi-plus Bell state, got {counts.get('01', 0)} counts."
    assert counts.get("10", 0) == 0, f"State '10' should not appear for a phi-plus Bell state, got {counts.get('10', 0)} counts."
    assert counts.get("00", 0) > 0, "State '00' should appear with nonzero counts for a phi-plus Bell state."
    assert counts.get("11", 0) > 0, "State '11' should appear with nonzero counts for a phi-plus Bell state."


def test_sampler_called_with_aer_backend_and_returns_counts_3():
    import builtins as _b
    from unittest.mock import patch
    from qiskit.primitives import StatevectorSampler

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    seen = {"mode": None, "init_called": False}

    class TrackingSampler:
        def __init__(self, mode=None, *args, **kwargs):
            seen["init_called"] = True
            seen["mode"] = mode
            self._sampler = StatevectorSampler(seed=999)

        def run(self, pubs, *args, **kwargs):
            if "shots" not in kwargs:
                kwargs["shots"] = 300
            return self._sampler.run(pubs, *args, **kwargs)

    with patch.dict(candidate.__globals__, {"Sampler": TrackingSampler}):
        counts = candidate()

    assert seen["init_called"], "Function must construct a Sampler instance."
    assert seen["mode"] is not None, "Sampler should be initialized with a backend/mode."
    mode_type_name = type(seen["mode"]).__name__
    assert "AerSimulator" in mode_type_name, f"Sampler should use an Aer simulator backend, got mode type {mode_type_name}."
    assert isinstance(counts, dict), "Function must return counts after running the sampler."
    assert set(counts.keys()) <= {"00", "11"}, f"Using the correct Bell-state circuit should only yield '00' and '11', got {set(counts.keys())}."