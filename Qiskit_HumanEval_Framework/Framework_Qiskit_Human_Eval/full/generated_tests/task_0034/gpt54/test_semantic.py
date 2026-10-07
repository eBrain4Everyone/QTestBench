# SEMANTIC tests — Qiskit HumanEval task task_0034
# Generated: 2026-04-28T12:36:56.919962
# Model: openai/gpt-5.4 (gpt54)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = "def check(candidate):\n    from numpy import isclose\n    jobs = candidate()\n    reference_data = {\n        'phi_plus': {'00': 0.10, '11': 0.10},\n        'phi_minus': {'00': 0.10, '11': 0.10},\n        'psi_plus': {'01': 0.10, '10': 0.10},\n        'psi_minus': {'01': 0.1, '10': 0.10}\n    }\n    assert isinstance(jobs, dict)\n    assert set(jobs.keys()) == set(reference_data.keys())\n    for state, job in jobs.items():\n        assert isinstance(job, PrimitiveJob)\n        assert job.job_id() is not None\n        counts = job.result()[0].data.meas.get_counts()\n        shots = 4096\n        normalized_counts = {k: v/shots for k, v in counts.items()}\n        for key, value in reference_data[state].items():\n            assert isclose(normalized_counts[key], value, atol=1e-01)\n"
ENTRY_POINT_NAME = 'run_jobs_on_batch'
# --- Official check block end ---
def test_return_structure_and_batch_ids_1():
    import builtins as _b
    import numpy as np
    from qiskit.primitives.primitive_job import PrimitiveJob

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    result = candidate()

    assert isinstance(result, dict), "run_jobs_on_batch must return a dictionary."
    expected_keys = {"phi_plus", "phi_minus", "psi_plus", "psi_minus"}
    assert set(result.keys()) == expected_keys, "Returned dictionary must have exactly the four Bell-state keys."

    batch_ids = []
    for key in expected_keys:
        value = result[key]
        assert isinstance(value, tuple), f"Value for key '{key}' must be a tuple containing (job, batch_id)."
        assert len(value) == 2, f"Value for key '{key}' must have length 2: (job, batch_id)."
        job, batch_id = value
        assert isinstance(job, PrimitiveJob), f"First element for key '{key}' must be a PrimitiveJob-compatible object."
        assert isinstance(batch_id, str), f"Second element for key '{key}' must be a batch id string."
        assert len(batch_id) > 0, f"Batch id for key '{key}' must be a non-empty string."
        batch_ids.append(batch_id)

    assert len(set(batch_ids)) == 1, "All returned jobs must belong to the same batch and therefore share the same batch id."


def test_sampler_distributions_match_four_bell_states_2():
    import builtins as _b
    import numpy as np

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    result = candidate()

    expected_supports = {
        "phi_plus": {"00", "11"},
        "phi_minus": {"00", "11"},
        "psi_plus": {"01", "10"},
        "psi_minus": {"01", "10"},
    }

    for name, (job, batch_id) in result.items():
        pub_result = job.result()
        assert len(pub_result) >= 1, f"Job result for '{name}' must contain at least one publication result."
        first = pub_result[0]

        bit_array = getattr(first.data, "meas", None)
        assert bit_array is not None, f"Job result for '{name}' must contain measurement data under data.meas."

        counts = bit_array.get_counts()
        assert isinstance(counts, dict) and len(counts) > 0, f"Measurement counts for '{name}' must be a non-empty dictionary."

        observed = set(counts.keys())
        assert observed.issubset(expected_supports[name]), (
            f"Observed outcomes for '{name}' must be restricted to the Bell-state support {expected_supports[name]}, "
            f"but got {observed}."
        )

        total = sum(counts.values())
        assert total > 0, f"Total counts for '{name}' must be positive."

        probs = {k: v / total for k, v in counts.items()}
        for bitstr in expected_supports[name]:
            p = probs.get(bitstr, 0.0)
            assert np.isclose(p, 0.5, atol=0.25, rtol=1e-5), (
                f"Bell state '{name}' should yield approximately equal weight on its two support states; "
                f"probability for '{bitstr}' was {p}."
            )

        forbidden = {"00", "01", "10", "11"} - expected_supports[name]
        forbidden_mass = sum(probs.get(bitstr, 0.0) for bitstr in forbidden)
        assert np.allclose(forbidden_mass, 0.0, atol=0.15, rtol=1e-5), (
            f"Bell state '{name}' should place negligible probability on forbidden outcomes {forbidden}, "
            f"but observed total forbidden mass {forbidden_mass}."
        )


def test_relative_phase_distinguishes_plus_and_minus_states_3():
    import builtins as _b
    import numpy as np

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    result = candidate()

    phase_expectations = {
        "phi_plus": 1.0,
        "phi_minus": -1.0,
        "psi_plus": 1.0,
        "psi_minus": -1.0,
    }

    for name, (job, batch_id) in result.items():
        pub_result = job.result()
        assert len(pub_result) >= 1, f"Job result for '{name}' must contain at least one publication result."
        first = pub_result[0]

        bit_array = getattr(first.data, "meas", None)
        assert bit_array is not None, f"Job result for '{name}' must expose measurement data under data.meas."

        counts = bit_array.get_counts()
        total = sum(counts.values())
        assert total > 0, f"Measurement counts for '{name}' must sum to a positive number."

        p00 = counts.get("00", 0) / total
        p01 = counts.get("01", 0) / total
        p10 = counts.get("10", 0) / total
        p11 = counts.get("11", 0) / total

        zz = p00 + p11 - p01 - p10
        xx = (p00 + p11 - p01 - p10) * phase_expectations[name]

        assert np.isclose(abs(zz), 1.0, atol=0.15, rtol=1e-5), (
            f"Bell state '{name}' must show perfect computational-basis parity correlation or anti-correlation; got ZZ={zz}."
        )

        support_even = name.startswith("phi")
        if support_even:
            assert p01 + p10 < 0.15, (
                f"State '{name}' should be an even-parity Bell state with negligible odd-parity outcomes; "
                f"observed odd-parity probability {p01 + p10}."
            )
        else:
            assert p00 + p11 < 0.15, (
                f"State '{name}' should be an odd-parity Bell state with negligible even-parity outcomes; "
                f"observed even-parity probability {p00 + p11}."
            )

        assert np.isclose(xx, phase_expectations[name], atol=0.2, rtol=1e-5), (
            f"State '{name}' should match the expected plus/minus phase signature; computed phase diagnostic was {xx} "
            f"but expected approximately {phase_expectations[name]}."
        )