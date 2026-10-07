# SEMANTIC tests — Qiskit HumanEval task task_0034
# Generated: 2026-04-28T11:30:03.453271
# Model: deepseek/deepseek-v3.2 (deepseekv32)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = "def check(candidate):\n    from numpy import isclose\n    jobs = candidate()\n    reference_data = {\n        'phi_plus': {'00': 0.10, '11': 0.10},\n        'phi_minus': {'00': 0.10, '11': 0.10},\n        'psi_plus': {'01': 0.10, '10': 0.10},\n        'psi_minus': {'01': 0.1, '10': 0.10}\n    }\n    assert isinstance(jobs, dict)\n    assert set(jobs.keys()) == set(reference_data.keys())\n    for state, job in jobs.items():\n        assert isinstance(job, PrimitiveJob)\n        assert job.job_id() is not None\n        counts = job.result()[0].data.meas.get_counts()\n        shots = 4096\n        normalized_counts = {k: v/shots for k, v in counts.items()}\n        for key, value in reference_data[state].items():\n            assert isclose(normalized_counts[key], value, atol=1e-01)\n"
ENTRY_POINT_NAME = 'run_jobs_on_batch'
# --- Official check block end ---
import builtins as _b
import numpy as np
import pytest

def test_batch_execution_and_job_structure_1():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    result = candidate()
    assert isinstance(result, dict), "Function must return a dictionary."
    expected_keys = ['phi_plus', 'phi_minus', 'psi_plus', 'psi_minus']
    assert set(result.keys()) == set(expected_keys), f"Dictionary keys must be exactly {expected_keys}."

    for key in expected_keys:
        entry = result[key]
        assert isinstance(entry, tuple) and len(entry) == 2, f"Value for {key} must be a 2_tuple (RuntimeJob, batch_id)."
        job, batch_id = entry
        # RuntimeJob is a subclass of PrimitiveJob in the qiskit_ibm_runtime context.
        # Use a more general check for PrimitiveJob.
        from qiskit.primitives.primitive_job import PrimitiveJob
        assert isinstance(job, PrimitiveJob), f"First element for {key} must be a PrimitiveJob (or RuntimeJob)."
        assert isinstance(batch_id, str), f"Second element for {key} must be a string batch id."
        assert batch_id, "Batch id must not be empty."

    # Ensure all batch ids are identical (same batch).
    batch_ids = [result[key][1] for key in expected_keys]
    assert len(set(batch_ids)) == 1, "All jobs must belong to the same batch (identical batch id)."
    print("All jobs have same batch id:", batch_ids[0])

def test_transpilation_and_circuit_properties_2():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    result = candidate()
    # We cannot directly inspect the transpiled circuits inside the RuntimeJob,
    # but we can check that the job.result() yields correct probabilities for Bell states.
    # However, the function only returns jobs, not results.
    # So we run the jobs to completion (they are fake jobs) and verify the distributions.
    from qiskit.primitives import PrimitiveResult
    from qiskit.primitives import SamplerResult
    from qiskit.quantum_info import Statevector

    bell_states = {
        'phi_plus': Statevector([1, 0, 0, 1]) / np.sqrt(2),
        'phi_minus': Statevector([1, 0, 0, -1]) / np.sqrt(2),
        'psi_plus': Statevector([0, 1, 1, 0]) / np.sqrt(2),
        'psi_minus': Statevector([0, 1, -1, 0]) / np.sqrt(2),
    }

    for key in bell_states:
        job = result[key][0]
        # Wait for job completion (fake backend will be immediate).
        r = job.result()
        # The result should have quasi_distributions for each circuit.
        # Since each batch job contains one circuit per Bell state,
        # we expect one quasi_distribution.
        assert hasattr(r, 'quasi_dists'), "Result must have quasi_dists attribute."
        qdists = r.quasi_dists
        assert len(qdists) == 1, "Expected exactly one quasi_distribution per job."
        qdist = qdists[0]
        # The quasi_distribution should be deterministic: all probability on one computational basis.
        # For a Bell state measured in computational basis, the distribution is uniform over 00 and 11 (or 01 and 10).
        # But because the transpiler may add measurements, we just check that the probabilities sum to 1.
        total_prob = sum(qdist.values())
        assert np.allclose(total_prob, 1.0, atol=1e-4), f"Quasi_distribution for {key} must sum to 1."
        # Check that the distribution is supported on two outcomes (00,11) or (01,10) depending on Bell state.
        # For phi_plus and phi_minus the support is {0,3}; for psi_plus and psi_minus the support is {1,2}.
        if key in ('phi_plus', 'phi_minus'):
            expected_support = {0, 3}
        else:
            expected_support = {1, 2}
        actual_support = set(qdist.keys())
        assert actual_support == expected_support, f"Support for {key} must be {expected_support}, got {actual_support}."
        # Each outcome should have probability 0.5
        for outcome in expected_support:
            assert np.allclose(qdist[outcome], 0.5, atol=1e-4), f"Outcome {outcome} for {key} must have probability 0.5."

def test_batch_mode_and_backend_consistency_3():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    result = candidate()
    # Verify that the batch id is consistent and that the jobs are created with the correct backend.
    from qiskit_ibm_runtime.fake_provider import FakeAlgiers
    # The function uses Batch and Sampler with FakeAlgiers.
    # We cannot directly inspect the batch object from the returned dict,
    # but we can ensure that each job's backend name matches FakeAlgiers.
    for key in ['phi_plus', 'phi_minus', 'psi_plus', 'psi_minus']:
        job = result[key][0]
        # In the fake provider, the job's backend attribute may not be set directly,
        # but we can check that the job is a PrimitiveJob and can be run to completion.
        # Actually run the job (already done in previous test) to ensure no errors.
        r = job.result()
        assert r is not None, f"Job for {key} must produce a result."

    # Additional check: all batch ids equal.
    batch_ids = [result[key][1] for key in ['phi_plus', 'phi_minus', 'psi_plus', 'psi_minus']]
    assert all(bid == batch_ids[0] for bid in batch_ids), "All batch ids must be identical."
    # Ensure batch id is a non_empty string.
    assert isinstance(batch_ids[0], str) and batch_ids[0], "Batch id must be a non_empty string."

    # Verify that the function returns exactly four entries.
    assert len(result) == 4, "Result dictionary must contain exactly four entries."