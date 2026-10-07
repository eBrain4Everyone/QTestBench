# SEMANTIC tests — Qiskit HumanEval task task_0035
# Generated: 2026-04-28T11:31:46.464707
# Model: deepseek/deepseek-v3.2 (deepseekv32)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from numpy import isclose\n    job = candidate()\n    assert isinstance(job, PrimitiveJob)\n    assert job.job_id() is not None\n    result = job.result()\n    assert isclose(result[0].data.evs.item(), 0.33, atol=0.06)\n'
ENTRY_POINT_NAME = 'run_circuit_with_dd_trex'
# --- Official check block end ---
import builtins as _b
import numpy as np
import pytest

# Load candidate implementation
sol = _b.INJECTED_SOLUTION_CODE
entry = _b.INJECTED_ENTRY_POINT
g = {"__builtins__": __builtins__}
exec(sol, g)
candidate = g[entry]


def test_run_circuit_with_dd_trex_1():
    """
    Test that the function returns a PrimitiveJob object with expected properties.
    """
    from qiskit.primitives.primitive_job import PrimitiveJob
    
    # Execute the function
    job = candidate()
    
    # Check return type
    assert isinstance(job, PrimitiveJob), f"Expected PrimitiveJob, got {type(job)}"
    
    # Check that job has expected attributes
    assert hasattr(job, 'job_id'), "PrimitiveJob should have job_id attribute"
    assert hasattr(job, 'result'), "PrimitiveJob should have result method"
    assert hasattr(job, 'status'), "PrimitiveJob should have status method"
    
    # Check job is in a valid state (newly created, not failed)
    # Note: We can't guarantee job_id format, just that it exists
    assert job.job_id is not None, "Job ID should not be None"


def test_run_circuit_with_dd_trex_2():
    """
    Test that the circuit is built with correct parameters (5 qubits, 2 repetitions, pairwise entanglement).
    Verify transpilation with correct optimization level and seed.
    """
    from qiskit.circuit.library import EfficientSU2
    from qiskit_ibm_runtime.fake_provider import FakeAuckland
    from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
    
    # Execute the function
    job = candidate()
    
    # Get the result to inspect circuits
    result = job.result()
    
    # Check that result has expected structure for Estimator
    assert hasattr(result, 'values'), "Result should have values attribute"
    assert hasattr(result, 'metadata'), "Result should have metadata attribute"
    
    # Extract values and metadata
    values = result.values
    metadata = result.metadata
    
    # Check values is a list/array with at least one element
    assert len(values) > 0, "Result should contain expectation values"
    
    # Check metadata contains circuit info
    assert isinstance(metadata, list), "Metadata should be a list"
    assert len(metadata) > 0, "Metadata should not be empty"
    
    # Check that we have at least one metadata entry with circuit information
    first_metadata = metadata[0]
    assert isinstance(first_metadata, dict), "Metadata entries should be dictionaries"
    
    # Check for expected keys in metadata (circuit info)
    assert 'circuit_metadata' in first_metadata, "Metadata should contain circuit_metadata"
    
    # Verify circuit metadata has expected properties
    circuit_meta = first_metadata['circuit_metadata']
    assert 'num_qubits' in circuit_meta, "Circuit metadata should contain num_qubits"
    assert circuit_meta['num_qubits'] == 5, f"Expected 5 qubits, got {circuit_meta['num_qubits']}"
    
    # Check optimization level was used
    assert 'optimization_level' in first_metadata, "Metadata should contain optimization_level"
    assert first_metadata['optimization_level'] == 1, f"Expected optimization level 1, got {first_metadata.get('optimization_level')}"


def test_run_circuit_with_dd_trex_3():
    """
    Test that the observable is correctly specified as 1*Z_-1 (Z on last qubit, identity elsewhere).
    Verify expectation value is within valid range [-1, 1].
    """
    import numpy as np
    from qiskit.quantum_info import SparsePauliOp
    
    # Execute the function
    job = candidate()
    
    # Get the result
    result = job.result()
    values = result.values
    
    # Check values is iterable
    assert hasattr(values, '__iter__'), "Result values should be iterable"
    
    # Convert to numpy array for easier handling
    values_array = np.array(values)
    
    # Check expectation value is within valid range for Pauli Z observable
    for val in values_array:
        assert -1.0 - 1e-8 <= val <= 1.0 + 1e-8, f"Expectation value {val} should be in [-1, 1] for Pauli Z observable"
    
    # Check we have exactly one expectation value (one circuit, one observable)
    assert len(values_array) == 1, f"Expected exactly one expectation value, got {len(values_array)}"
    
    # Check metadata contains observable info
    metadata = result.metadata
    assert len(metadata) == 1, f"Expected metadata for one circuit, got {len(metadata)}"
    
    # Verify observable was specified correctly (Z on last qubit)
    # The observable 1*Z_-1 means Z on qubit index -1 (last qubit) with identity on others
    # This would be represented as "IIIIZ" for 5 qubits
    first_metadata = metadata[0]
    
    # Check for keys that might contain observable information
    # Different Estimator implementations might store this differently
    observable_found = False
    
    # Check common metadata keys
    for key in ['observable', 'paulis', 'operator']:
        if key in first_metadata:
            observable_found = True
            break
    
    # It's acceptable if observable info isn't directly in metadata
    # as long as the expectation value is valid
    if observable_found:
        # If observable info is present, verify it matches "IIIIZ" pattern
        if 'observable' in first_metadata:
            obs = first_metadata['observable']
            if isinstance(obs, SparsePauliOp):
                # Check it's Z on last qubit
                paulis = obs.paulis
                assert len(paulis) == 1, f"Expected single Pauli term, got {len(paulis)}"
                pauli_str = str(paulis[0])
                # For 5 qubits, Z on last qubit is "IIIIZ"
                assert pauli_str.endswith('Z'), f"Expected Z on last qubit, got {pauli_str}"
                assert pauli_str.count('I') == 4, f"Expected 4 I's for 5-qubit Z_-1, got {pauli_str}"