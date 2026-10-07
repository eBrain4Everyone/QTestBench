# SYNTACTIC tests — Qiskit HumanEval task task_0002
# Generated: 2026-04-28T11:39:57.981209
# Model: google/gemini-3.1-pro-preview (gemini3pro)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    solution = (Statevector.from_label("00") + Statevector.from_label("11")) / sqrt(2)\n    assert result.equiv(solution)\n'
ENTRY_POINT_NAME = 'create_bell_statevector'
# --- Official check block end ---
def test_syntax_and_callable_1():
    import builtins as _b
    import ast
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    
    try:
        ast.parse(sol)
    except SyntaxError as e:
        assert False, f"Syntax error in solution code: {e}"
        
    g = {"__builtins__": __builtins__}
    try:
        exec(sol, g)
    except Exception as e:
        assert False, f"Execution of solution code failed: {e}"
        
    assert entry in g, f"Entry point '{entry}' not found in the executed namespace."
    assert callable(g[entry]), f"Entry point '{entry}' is not callable."

def test_signature_2():
    import builtins as _b
    import inspect
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    sig = inspect.signature(candidate)
    assert len(sig.parameters) == 0, f"Expected function '{entry}' to take 0 arguments, but it takes {len(sig.parameters)}."

def test_return_type_3():
    import builtins as _b
    from qiskit.quantum_info import Statevector
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    result = candidate()
    assert isinstance(result, Statevector), f"Function '{entry}' should return a qiskit.quantum_info.Statevector object, got {type(result)}."
    assert result.dim == 4, f"Expected a 2-qubit statevector (dimension 4), but got dimension {result.dim}."