# SYNTACTIC tests — Qiskit HumanEval task task_0020
# Generated: 2026-04-28T11:12:05.305069
# Model: anthropic/claude-opus-4-6 (claudeopus46)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    result.remove_final_measurements()\n    backend = FakePerth()\n    assert result.num_qubits == backend.num_qubits\n    assert result.layout.initial_index_layout()[:3] == [2, 4, 6]\n'
ENTRY_POINT_NAME = 'transpile_ghz_customlayout'
# --- Official check block end ---
import ast
import inspect

def test_module_parses_and_loads_1():
    """Test that the solution source parses as valid Python and executes without error."""
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    # Check that the source is valid Python
    tree = ast.parse(sol)
    assert tree is not None, "ast.parse returned None; source is not valid Python"

    # Check that exec succeeds
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    assert entry in g, f"Entry point '{entry}' not found in executed module namespace"


def test_entry_point_exists_and_callable_2():
    """Test that the entry point exists, is callable, and has the correct signature (no parameters)."""
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    g = {"__builtins__": __builtins__}
    exec(sol, g)

    candidate = g[entry]
    assert callable(candidate), f"'{entry}' is not callable"

    sig = inspect.signature(candidate)
    params = [
        p for p in sig.parameters.values()
        if p.default is inspect.Parameter.empty
        and p.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
    ]
    assert len(params) == 0, (
        f"'{entry}' should take no required arguments, but has required params: {params}"
    )


def test_return_type_is_quantum_circuit_3():
    """Test that calling the entry point returns a QuantumCircuit instance."""
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    g = {"__builtins__": __builtins__}
    exec(sol, g)

    candidate = g[entry]
    result = candidate()

    from qiskit import QuantumCircuit
    assert isinstance(result, QuantumCircuit), (
        f"Expected return type QuantumCircuit, got {type(result).__name__}"
    )