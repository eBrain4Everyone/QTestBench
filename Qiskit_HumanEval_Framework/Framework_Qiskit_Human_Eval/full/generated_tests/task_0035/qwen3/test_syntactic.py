# SYNTACTIC tests — Qiskit HumanEval task task_0035
# Generated: 2026-04-28T12:42:12.645336
# Model: qwen/qwen3-coder-next (qwen3)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from numpy import isclose\n    job = candidate()\n    assert isinstance(job, PrimitiveJob)\n    assert job.job_id() is not None\n    result = job.result()\n    assert isclose(result[0].data.evs.item(), 0.33, atol=0.06)\n'
ENTRY_POINT_NAME = 'run_circuit_with_dd_trex'
# --- Official check block end ---
import ast
import inspect
import builtins as _b

# Load the solution and entry point
sol = _b.INJECTED_SOLUTION_CODE
entry = _b.INJECTED_ENTRY_POINT

def test_module_syntax_and_imports():
    """Verify solution source parses correctly and imports succeed."""
    # Parse solution AST to check syntax
    ast.parse(sol)
    
    # Build namespace and exec
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    
    # Check required imports are available in solution context
    required_modules = [
        'qiskit.circuit.library.efficient_su2',
        'qiskit.quantum_info.SparsePauliOp',
        'qiskit.transpiler.CouplingMap',
        'numpy',
        'qiskit_ibm_runtime.Estimator',
        'qiskit_ibm_runtime.EstimatorOptions',
        'qiskit.primitives.primitive_job.PrimitiveJob',
        'qiskit_ibm_runtime.fake_provider.FakeAuckland',
        'qiskit.transpiler.preset_passmanagers.generate_preset_pass_manager'
    ]
    
    # Just ensure the code can be imported; actual function call is in next test
    assert 'efficient_su2' in g or 'qiskit' in g, "Failed to import efficient_su2"
    assert 'numpy' in g or 'np' in g, "Failed to import numpy"

def test_entry_point_exists_and_is_callable():
    """Verify entry point function exists and is callable."""
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    
    assert entry in g, f"Entry point '{entry}' not found in solution"
    candidate = g[entry]
    assert callable(candidate), f"Entry point '{entry}' is not callable"

def test_entry_point_signature_and_return_type():
    """Verify entry point has correct signature and returns expected type."""
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    
    candidate = g[entry]
    
    # Check it's callable (already tested above, but keep for completeness)
    assert callable(candidate), f"Entry point '{entry}' must be callable"
    
    # Try calling it and check return type
    result = candidate()
    
    # Import needed types locally for checking
    from qiskit.primitives.primitive_job import PrimitiveJob
    assert isinstance(result, PrimitiveJob), f"Expected PrimitiveJob, got {type(result)}"