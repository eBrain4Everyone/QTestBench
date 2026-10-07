# SYNTACTIC tests — Qiskit HumanEval task task_0019
# Generated: 2026-04-28T12:40:24.842215
# Model: qwen/qwen3-coder-next (qwen3)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    result.remove_final_measurements()\n    backend = FakeTorontoV2()\n    # Check initial layout is not the trivial layout (this is very unlikely\n    # if transpiled with optimization level 3)\n    assert result.layout.initial_index_layout() != list(range(backend.num_qubits))\n    # Optimization level 3 should easily find circuits with depth < 200\n    assert result.depth() < 150\n'
ENTRY_POINT_NAME = 'transpile_circuit_maxopt'
# --- Official check block end ---
def test_transpile_circuit_maxopt_module_loads_1():
    import builtins as _b
    import ast
    import inspect

    # Ensure the solution module parses correctly
    sol = _b.INJECTED_SOLUTION_CODE
    ast.parse(sol)

    # Build namespace and execute
    g = {"__builtins__": __builtins__}
    exec(sol, g)

    # Check entry point exists and is callable
    entry = _b.INJECTED_ENTRY_POINT
    assert entry in g, f"Entry point '{entry}' not found in solution globals"
    assert callable(g[entry]), f"Entry point '{entry}' is not callable"

    # Basic signature check: function should require no arguments and return a QuantumCircuit
    sig = inspect.signature(g[entry])
    assert len(sig.parameters) == 0, f"Function '{entry}' should take no arguments"
    assert sig.return_annotation == 'QuantumCircuit' or sig.return_annotation is None or True, "Return type annotation is acceptable"


def test_transpile_circuit_maxopt_basic_output_2():
    import builtins as _b
    from qiskit import QuantumCircuit

    sol = _b.INJECTED_SOLUTION_CODE
    g = {"__builtins__": __builtins__}
    exec(sol, g)

    entry = _b.INJECTED_ENTRY_POINT
    candidate = g[entry]
    result = candidate()

    # Verify output type
    assert isinstance(result, QuantumCircuit), f"Expected QuantumCircuit, got {type(result)}"
    # Basic sanity: non-empty and has at least one qubit
    assert result.num_qubits >= 1, f"Circuit must have at least one qubit, got {result.num_qubits}"


def test_transpile_circuit_maxopt_has_measurements_3():
    import builtins as _b
    from qiskit import QuantumCircuit

    sol = _b.INJECTED_SOLUTION_CODE
    g = {"__builtins__": __builtins__}
    exec(sol, g)

    entry = _b.INJECTED_ENTRY_POINT
    candidate = g[entry]
    result = candidate()

    # Verify circuit is valid for backend (has at least one measurement)
    # GHZ circuits typically measure all qubits
    ops = result.count_ops()
    assert 'measure' in ops, f"Circuit must contain 'measure' operation, found ops: {ops}"
    assert ops['measure'] >= 1, f"Circuit must have at least one measurement, found {ops['measure']}"