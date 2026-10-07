# SYNTACTIC tests — Qiskit HumanEval task task_0002
# Generated: 2026-04-28T11:09:43.031880
# Model: anthropic/claude-opus-4-6 (claudeopus46)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    solution = (Statevector.from_label("00") + Statevector.from_label("11")) / sqrt(2)\n    assert result.equiv(solution)\n'
ENTRY_POINT_NAME = 'create_bell_statevector'
# --- Official check block end ---
import ast
import inspect

def test_module_parses_and_loads_1():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    # Check that the solution source is valid Python
    tree = ast.parse(sol)
    assert tree is not None, "Solution source should be parseable as valid Python"

    # Check that exec succeeds
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    assert entry in g, f"Entry point '{entry}' should exist in the executed namespace"


def test_entry_point_is_callable_2():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    g = {"__builtins__": __builtins__}
    exec(sol, g)

    candidate = g[entry]
    assert callable(candidate), f"'{entry}' should be callable"

    # Check signature: should take no arguments (besides possibly self, but it's a function)
    sig = inspect.signature(candidate)
    params = [
        p for p in sig.parameters.values()
        if p.default is inspect.Parameter.empty
        and p.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
    ]
    assert len(params) == 0, (
        f"'{entry}' should require no arguments, but has required params: {params}"
    )


def test_return_type_is_statevector_3():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    from qiskit.quantum_info import Statevector

    g = {"__builtins__": __builtins__}
    exec(sol, g)

    candidate = g[entry]
    result = candidate()
    assert isinstance(result, Statevector), (
        f"Return value should be a Statevector instance, got {type(result)}"
    )
    # Plausibility: Bell state is a 2-qubit state, so dimension should be 4
    assert result.dim == 4, (
        f"Bell state should have dimension 4 (2 qubits), got {result.dim}"
    )