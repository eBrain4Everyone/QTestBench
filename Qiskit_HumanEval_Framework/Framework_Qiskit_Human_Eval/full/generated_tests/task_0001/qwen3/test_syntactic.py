# SYNTACTIC tests — Qiskit HumanEval task task_0001
# Generated: 2026-04-28T12:38:57.805633
# Model: qwen/qwen3-coder-next (qwen3)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    assert isinstance(result, dict)\n    assert result.keys() == {"00", "11"}\n    assert 0.4 < (result["00"] / sum(result.values())) < 0.6\n'
ENTRY_POINT_NAME = 'run_bell_state_simulator'
# --- Official check block end ---
import ast
import inspect
import builtins as _b


def test_module_loads_and_entry_exists_1():
    # Verify syntax and basic structure
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    
    # Parse source to check syntax
    ast.parse(sol)
    
    # Build namespace and execute
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    
    # Check entry point exists
    assert entry in g, f"Entry point '{entry}' not found in module namespace"
    
    # Check it's callable
    func = g[entry]
    assert callable(func), f"'{entry}' is not callable"


def test_entry_point_signature_2():
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    
    func = g[entry]
    sig = inspect.signature(func)
    
    # Entry point should take no arguments (as per problem statement)
    params = list(sig.parameters.keys())
    assert len(params) == 0, f"Expected no parameters, got {params}"


def test_entry_point_returns_dict_3():
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    
    func = g[entry]
    
    # Call with no args and check return type
    result = func()
    
    # According to prompt, should return a counts dictionary
    assert isinstance(result, dict), f"Expected dict, got {type(result)}"