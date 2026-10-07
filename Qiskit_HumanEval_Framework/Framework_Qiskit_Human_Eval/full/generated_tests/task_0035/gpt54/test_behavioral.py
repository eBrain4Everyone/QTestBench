# BEHAVIORAL tests — Qiskit HumanEval task task_0035
# Generated: 2026-04-28T12:38:03.020711
# Model: openai/gpt-5.4 (gpt54)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from numpy import isclose\n    job = candidate()\n    assert isinstance(job, PrimitiveJob)\n    assert job.job_id() is not None\n    result = job.result()\n    assert isclose(result[0].data.evs.item(), 0.33, atol=0.06)\n'
ENTRY_POINT_NAME = 'run_circuit_with_dd_trex'
# --- Official check block end ---
def test_returns_primitive_job_1():
    import builtins as _b
    g = {"__builtins__": __builtins__}
    exec(_b.INJECTED_SOLUTION_CODE, g)
    candidate = g[_b.INJECTED_ENTRY_POINT]

    result = candidate()

    from qiskit.primitives.primitive_job import PrimitiveJob
    assert isinstance(result, PrimitiveJob), "The function must return a qiskit PrimitiveJob instance."

    job_result = result.result()
    assert job_result is not None, "The returned PrimitiveJob should produce a non-None result when awaited."


def test_expectation_value_matches_reference_2():
    import builtins as _b
    import numpy as np
    g = {"__builtins__": __builtins__}
    exec(_b.INJECTED_SOLUTION_CODE, g)
    candidate = g[_b.INJECTED_ENTRY_POINT]

    user_job = candidate()
    user_res = user_job.result()

    user_ev = None
    if hasattr(user_res, "values"):
        vals = user_res.values
        if len(vals) > 0:
            user_ev = float(vals[0])
    elif hasattr(user_res, "__getitem__"):
        try:
            first = user_res[0]
            if hasattr(first, "data") and hasattr(first.data, "evs"):
                data_evs = first.data.evs
                user_ev = float(data_evs[0] if hasattr(data_evs, "__len__") else data_evs)
        except Exception:
            pass

    assert user_ev is not None, "Could not extract an expectation value from the returned PrimitiveJob result."

    from qiskit.circuit.library import efficient_su2
    from qiskit.quantum_info import SparsePauliOp
    from qiskit_ibm_runtime import Estimator, EstimatorOptions
    from qiskit_ibm_runtime.fake_provider import FakeAuckland
    from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

    backend = FakeAuckland()
    circuit = efficient_su2(5, reps=2, entanglement="pairwise")
    observable = SparsePauliOp.from_list([("IIIIZ", 1.0)])

    pm = generate_preset_pass_manager(
        backend=backend,
        optimization_level=1,
        seed_transpiler=789,
    )
    isa_circuit = pm.run(circuit)
    isa_obs = observable.apply_layout(isa_circuit.layout)

    options = EstimatorOptions()
    ref_estimator = Estimator(mode=backend, options=options)
    ref_job = ref_estimator.run([(isa_circuit, isa_obs)])
    ref_res = ref_job.result()

    ref_ev = None
    if hasattr(ref_res, "values"):
        vals = ref_res.values
        if len(vals) > 0:
            ref_ev = float(vals[0])
    elif hasattr(ref_res, "__getitem__"):
        first = ref_res[0]
        if hasattr(first, "data") and hasattr(first.data, "evs"):
            data_evs = first.data.evs
            ref_ev = float(data_evs[0] if hasattr(data_evs, "__len__") else data_evs)

    assert ref_ev is not None, "Reference computation failed to produce an extractable expectation value."
    assert np.allclose(user_ev, ref_ev, atol=1e-4, rtol=1e-5), (
        f"Expectation value mismatch: got {user_ev}, expected approximately {ref_ev} "
        "for EfficientSU2(5, reps=2, entanglement='pairwise') with FakeAuckland, "
        "optimization_level=1, seed_transpiler=789, and observable 1*Z_-1."
    )


def test_result_structure_and_physical_range_3():
    import builtins as _b
    import numpy as np
    g = {"__builtins__": __builtins__}
    exec(_b.INJECTED_SOLUTION_CODE, g)
    candidate = g[_b.INJECTED_ENTRY_POINT]

    job = candidate()
    res = job.result()

    ev = None
    std = None

    if hasattr(res, "values"):
        vals = res.values
        assert len(vals) == 1, "The estimator result should contain exactly one expectation value for one circuit-observable pair."
        ev = float(vals[0])
        if hasattr(res, "metadata"):
            meta = res.metadata
            assert len(meta) == 1, "Metadata should have exactly one entry corresponding to the single estimator input."
    elif hasattr(res, "__getitem__"):
        first = res[0]
        if hasattr(first, "data") and hasattr(first.data, "evs"):
            data_evs = first.data.evs
            ev = float(data_evs[0] if hasattr(data_evs, "__len__") else data_evs)
        if hasattr(first, "data") and hasattr(first.data, "stds"):
            data_stds = first.data.stds
            std = float(data_stds[0] if hasattr(data_stds, "__len__") else data_stds)

    assert ev is not None, "The job result must expose a single numeric expectation value."
    assert np.isfinite(ev), "The expectation value must be a finite real number."
    assert -1.0001 <= ev <= 1.0001, "The expectation value of a Pauli-Z observable must lie within [-1, 1]."
    if std is not None:
        assert std >= 0.0, "Reported standard deviation/uncertainty must be non-negative."