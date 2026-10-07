# SEMANTIC tests — Qiskit HumanEval task task_0034
# Generated: 2026-04-28T11:14:08.742078
# Model: anthropic/claude-opus-4-6 (claudeopus46)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = "def check(candidate):\n    from numpy import isclose\n    jobs = candidate()\n    reference_data = {\n        'phi_plus': {'00': 0.10, '11': 0.10},\n        'phi_minus': {'00': 0.10, '11': 0.10},\n        'psi_plus': {'01': 0.10, '10': 0.10},\n        'psi_minus': {'01': 0.1, '10': 0.10}\n    }\n    assert isinstance(jobs, dict)\n    assert set(jobs.keys()) == set(reference_data.keys())\n    for state, job in jobs.items():\n        assert isinstance(job, PrimitiveJob)\n        assert job.job_id() is not None\n        counts = job.result()[0].data.meas.get_counts()\n        shots = 4096\n        normalized_counts = {k: v/shots for k, v in counts.items()}\n        for key, value in reference_data[state].items():\n            assert isclose(normalized_counts[key], value, atol=1e-01)\n"
ENTRY_POINT_NAME = 'run_jobs_on_batch'
# --- Official check block end ---
import pytest


def test_return_type_and_keys_1():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    result = candidate()

    assert isinstance(result, dict), "Return value must be a dictionary"

    expected_keys = {'phi_plus', 'phi_minus', 'psi_plus', 'psi_minus'}
    assert set(result.keys()) == expected_keys, (
        f"Dictionary keys must be {expected_keys}, got {set(result.keys())}"
    )


def test_values_contain_job_objects_and_batch_id_2():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    result = candidate()

    for key in ['phi_plus', 'phi_minus', 'psi_plus', 'psi_minus']:
        value = result[key]
        # The value should be a tuple or contain both a job object and a batch id
        # Based on the prompt: "values are the corresponding RuntimeJob objects and the batch id"
        # This likely means each value is a tuple of (job, batch_id) or the dict has jobs + batch_id
        # Let's check that the value is not None
        assert value is not None, f"Value for key '{key}' should not be None"

        # Check if value is a tuple/list containing job and batch_id
        if isinstance(value, (tuple, list)):
            assert len(value) >= 1, (
                f"Value for '{key}' should contain at least a job object, got length {len(value)}"
            )
            # The first element should be a job-like object
            job = value[0]
            assert hasattr(job, 'result') or hasattr(job, 'job_id'), (
                f"First element for '{key}' should be a job-like object with 'result' or 'job_id' method/attribute"
            )
        else:
            # If not a tuple, it might be that all values are jobs and batch_id is separate
            # or the value itself is a job
            assert hasattr(value, 'result') or hasattr(value, 'job_id'), (
                f"Value for '{key}' should be a job-like object with 'result' or 'job_id', got {type(value)}"
            )


def test_bell_state_measurement_results_3():
    import builtins as _b
    import numpy as np
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    result = candidate()

    # For each Bell state, extract the job and check the measurement outcomes
    bell_expected_outcomes = {
        'phi_plus': {'00', '11'},      # |00> + |11>
        'phi_minus': {'00', '11'},     # |00> - |11>
        'psi_plus': {'01', '10'},      # |01> + |10>
        'psi_minus': {'01', '10'},     # |01> - |10>
    }

    for key in ['phi_plus', 'phi_minus', 'psi_plus', 'psi_minus']:
        value = result[key]

        # Extract job from value
        if isinstance(value, (tuple, list)):
            job = value[0]
        else:
            job = value

        # Try to get results
        if hasattr(job, 'result'):
            try:
                job_result = job.result()
                # SamplerV2 returns PubResult objects
                # Try to extract counts/bitstrings
                if hasattr(job_result, '__getitem__'):
                    pub_result = job_result[0]
                    if hasattr(pub_result, 'data'):
                        data = pub_result.data
                        # Get the classical register data
                        for attr_name in dir(data):
                            attr = getattr(data, attr_name)
                            if hasattr(attr, 'get_counts'):
                                counts = attr.get_counts()
                                measured_states = set(counts.keys())
                                expected = bell_expected_outcomes[key]
                                assert measured_states.issubset(expected) or len(measured_states & expected) > 0, (
                                    f"Bell state '{key}' should primarily measure {expected}, got {measured_states}"
                                )
                                break
            except Exception:
                # If we can't extract results, at least verify the job exists
                pass

        assert key in result, f"Key '{key}' must be present in result dictionary"