# SYNTACTIC tests — Qiskit HumanEval task task_0000
# Generated: 2026-04-28T11:07:39.834443
# Model: anthropic/claude-opus-4-6 (claudeopus46)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate(3)\n    assert isinstance(result, QuantumCircuit)\n    assert result.num_qubits == 3\n'
ENTRY_POINT_NAME = 'create_quantum_circuit'
# --- Official check block end ---
import ast
import inspect

def test_module_loads_and_parses_1():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    # Test that the solution source is valid Python
    tree = ast.parse(sol)
    assert tree is not None, "Solution source should be parseable by ast.parse"

    # Test that exec succeeds
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

    # Check signature accepts at least one positional argument (n_qubits)
    sig = inspect.signature(candidate)
    params = list(sig.parameters.values())
    assert len(params) >= 1, (
        f"'{entry}' should accept at least one parameter (n_qubits), "
        f"but has {len(params)} parameters"
    )
    # The first parameter should accept a positional argument
    first_param = params[0]
    assert first_param.kind in (
        inspect.Parameter.POSITIONAL_ONLY,
        inspect.Parameter.POSITIONAL_OR_KEYWORD,
    ), f"First parameter '{first_param.name}' should accept positional arguments"


def test_basic_return_type_plausibility_3():
    import builtins as _b
    from qiskit import QuantumCircuit
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT

    g = {"__builtins__": __builtins__}
    exec(sol, g)

    candidate = g[entry]

    # Call with a simple argument and check the return type is QuantumCircuit
    result = candidate(3)
    assert isinstance(result, QuantumCircuit), (
        f"'{entry}(3)' should return a QuantumCircuit instance, got {type(result)}"
    )
    # Basic plausibility: the circuit should have the requested number of qubits
    assert result.num_qubits == 3, (
        f"'{entry}(3)' should return a circuit with 3 qubits, got {result.num_qubits}"
    )