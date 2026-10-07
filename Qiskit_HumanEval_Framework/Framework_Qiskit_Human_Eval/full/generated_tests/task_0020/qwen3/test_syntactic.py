# SYNTACTIC tests — Qiskit HumanEval task task_0020
# Generated: 2026-04-28T12:40:58.130127
# Model: qwen/qwen3-coder-next (qwen3)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    result.remove_final_measurements()\n    backend = FakePerth()\n    assert result.num_qubits == backend.num_qubits\n    assert result.layout.initial_index_layout()[:3] == [2, 4, 6]\n'
ENTRY_POINT_NAME = 'transpile_ghz_customlayout'
# --- Official check block end ---
def test_module_loads_and_entry_exists():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    g = {"__builtins__": __builtins__}
    import ast
    # Verify AST parses successfully
    ast.parse(sol)
    # Verify exec succeeds
    exec(sol, g)
    entry = _b.INJECTED_ENTRY_POINT
    assert entry == "transpile_ghz_customlayout"
    # Check entry point exists and is callable
    assert entry in g
    candidate = g[entry]
    from inspect import signature
    sig = signature(candidate)
    assert callable(candidate)
    assert len(sig.parameters) == 0
    # Return type hint must be QuantumCircuit
    assert sig.return_annotation == "QuantumCircuit"

def test_function_runs_and_returns_circuit():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    entry = _b.INJECTED_ENTRY_POINT
    candidate = g[entry]
    from qiskit import QuantumCircuit
    result = candidate()
    assert isinstance(result, QuantumCircuit)

def test_circuit_has_three_qubits_ghz_layout():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    entry = _b.INJECTED_ENTRY_POINT
    candidate = g[entry]
    from qiskit import QuantumCircuit
    circ = candidate()
    # Circuit should be a GHZ on 3 qubits
    assert circ.num_qubits == 3
    # Verify it's GHZ: hadamard on first, then CNOT chain, then hadamard on first again
    # Check structure: H0, CNOT(0,1), CNOT(1,2), H0
    # For custom layout [2,4,6] means physical qubits used; but structure should match GHZ
    from qiskit.quantum_info import Statevector
    sv = Statevector.from_instruction(circ)
    # GHZ state: (|000> + |111>) / sqrt(2)
    expected_ghz = (0.5**0.5) * (circ.from_except([0,1,2], 0) + circ.from_except([0,1,2], 7))
    # Compare fidelity
    fidelity = abs(sv.inner_product(expected_ghz))
    assert abs(fidelity - 1.0) < 1e-4