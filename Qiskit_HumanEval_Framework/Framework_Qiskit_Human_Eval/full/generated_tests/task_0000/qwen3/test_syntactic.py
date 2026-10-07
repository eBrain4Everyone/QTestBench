# SYNTACTIC tests — Qiskit HumanEval task task_0000
# Generated: 2026-04-28T12:38:42.252401
# Model: qwen/qwen3-coder-next (qwen3)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate(3)\n    assert isinstance(result, QuantumCircuit)\n    assert result.num_qubits == 3\n'
ENTRY_POINT_NAME = 'create_quantum_circuit'
# --- Official check block end ---
def test_create_quantum_circuit_module_loads_and_entry_exists():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    import ast
    # Verify the solution parses without syntax errors
    ast.parse(sol)
    # Verify exec succeeds
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    # Verify entry point exists and is callable
    assert hasattr(g, entry) or entry in g
    candidate = g[entry]
    assert callable(candidate)


def test_create_quantum_circuit_basic_signature():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    import inspect
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    sig = inspect.signature(candidate)
    params = list(sig.parameters.keys())
    # Should accept exactly one positional parameter
    assert len(params) == 1
    assert params[0] == 'n_qubits'


def test_create_quantum_circuit_returns_quantum_circuit():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    from qiskit import QuantumCircuit
    # Test with a small valid input
    circuit = candidate(3)
    assert isinstance(circuit, QuantumCircuit)
    assert circuit.num_qubits == 3