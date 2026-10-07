# SEMANTIC tests — Qiskit HumanEval task task_0035
# Generated: 2026-04-28T12:37:47.860113
# Model: openai/gpt-5.4 (gpt54)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from numpy import isclose\n    job = candidate()\n    assert isinstance(job, PrimitiveJob)\n    assert job.job_id() is not None\n    result = job.result()\n    assert isclose(result[0].data.evs.item(), 0.33, atol=0.06)\n'
ENTRY_POINT_NAME = 'run_circuit_with_dd_trex'
# --- Official check block end ---
def test_returns_primitive_job_and_result_structure_1():
    import builtins as _b
    import numpy as np
    from qiskit.primitives.primitive_job import PrimitiveJob

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    job = candidate()

    assert isinstance(job, PrimitiveJob), "The function must return a qiskit PrimitiveJob instance."

    result = job.result()
    assert result is not None, "The returned PrimitiveJob must produce a non-None result."
    assert hasattr(result, "__len__"), "Estimator result should be a sized container."
    assert len(result) == 1, "The Estimator job should contain exactly one published result for one circuit-observable pair."

    first = result[0]
    assert hasattr(first, "data"), "Each published estimator result should expose a 'data' attribute."
    assert hasattr(first.data, "evs"), "Estimator result data should contain expectation values in 'evs'."

    evs = np.asarray(first.data.evs)
    assert evs.size == 1, "There should be exactly one expectation value for the single observable."
    assert np.isfinite(float(evs.reshape(-1)[0])), "Expectation value must be a finite real number."


def test_expectation_value_matches_reconstructed_pipeline_2():
    import builtins as _b
    import numpy as np
    from qiskit.circuit.library import efficient_su2
    from qiskit.quantum_info import SparsePauliOp
    from qiskit_ibm_runtime import Estimator, EstimatorOptions
    from qiskit_ibm_runtime.fake_provider import FakeAuckland
    from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    job = candidate()
    got = float(np.asarray(job.result()[0].data.evs).reshape(-1)[0])

    backend = FakeAuckland()
    circuit = efficient_su2(5, reps=2, entanglement="pairwise")
    observable = SparsePauliOp("IIIIZ", coeffs=[1.0])

    pm = generate_preset_pass_manager(
        backend=backend,
        optimization_level=1,
        seed_transpiler=789,
    )
    tcircuit = pm.run(circuit)
    tobservable = observable.apply_layout(tcircuit.layout)

    options = EstimatorOptions(default_shots=4096)
    reference_job = Estimator(mode=backend, options=options).run([(tcircuit, tobservable)])
    expected = float(np.asarray(reference_job.result()[0].data.evs).reshape(-1)[0])

    assert np.allclose(got, expected, atol=1e-4, rtol=1e-5), (
        f"Expectation value should match the spec pipeline on FakeAuckland with seed 789; got {got}, expected {expected}."
    )


def test_value_is_valid_z_expectation_and_not_trivial_3():
    import builtins as _b
    import numpy as np

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    job = candidate()
    val = float(np.asarray(job.result()[0].data.evs).reshape(-1)[0])

    assert -1.0001 <= val <= 1.0001, (
        f"A single-qubit Z expectation value must lie within [-1, 1], but got {val}."
    )
    assert np.isfinite(val), "The expectation value must be finite."
    assert not np.allclose(val, 0.0, atol=1e-4, rtol=1e-5), (
        "For the specified EfficientSU2 circuit on FakeAuckland, the expectation should be nontrivial and not numerically zero."
    )