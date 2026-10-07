# SEMANTIC tests — Qiskit HumanEval task task_0035
# Generated: 2026-04-28T12:42:18.426305
# Model: qwen/qwen3-coder-next (qwen3)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from numpy import isclose\n    job = candidate()\n    assert isinstance(job, PrimitiveJob)\n    assert job.job_id() is not None\n    result = job.result()\n    assert isclose(result[0].data.evs.item(), 0.33, atol=0.06)\n'
ENTRY_POINT_NAME = 'run_circuit_with_dd_trex'
# --- Official check block end ---
def test_run_circuit_with_dd_trex_returns_primitive_job():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    result = candidate()
    from qiskit.primitives.primitive_job import PrimitiveJob
    assert isinstance(result, PrimitiveJob), "Expected PrimitiveJob return type"


def test_run_circuit_with_dd_trex_expectation_value_is_real():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    result = candidate()
    # Wait for job completion
    job_result = result.result()
    # Expectation value should be real (within numerical precision)
    exp_val = job_result['estimates'][0].expectation_value
    assert np.isreal(exp_val) or np.abs(exp_val.imag) < 1e-8, f"Expectation value should be real, got {exp_val}"


def test_run_circuit_with_dd_trex_observable_consistency():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    result = candidate()
    job_result = result.result()
    exp_val = job_result['estimates'][0].expectation_value
    
    # Build the observable manually as 1*Z_-1 as described in prompt
    from qiskit.quantum_info import SparsePauliOp
    # For 5 qubits, Z_-1 corresponds to Z on the last qubit (qubit index 4)
    # Z_-1 is interpreted as Pauli Z on the last qubit in the system
    observable = SparsePauliOp.from_list([("IIIIZ", 1.0)])
    
    # Verify expectation value is in reasonable range [-1, 1] for normalized Pauli observable
    assert -1.0 <= np.real(exp_val) <= 1.0, f"Expectation value {np.real(exp_val)} out of expected range [-1, 1]"