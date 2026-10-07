# SYNTACTIC tests — Qiskit HumanEval task task_0063
# Generated: 2026-04-28T12:10:05.595394
# Model: google/gemini-3.1-pro-preview (gemini3pro)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from numpy.random import seed\n    seed(12345)\n    basis = [1, 0, 0, 1, 1]\n    circuit = QuantumCircuit(5)\n    circuit.x([3, 4])\n    circuit.h([0, 3, 4])\n    result = candidate(basis, circuit)\n    assert result == "1"\n'
ENTRY_POINT_NAME = 'bb84_circuit_generate_key'
# --- Official check block end ---
import builtins as _b
import ast
import inspect
import warnings
from qiskit import QuantumCircuit

def test_ast_parse_and_execution_1():
    import builtins as _b
    import ast
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    
    try:
        ast.parse(sol)
    except SyntaxError as e:
        assert False, f"Syntax error in candidate code: {e}"
        
    g = {"__builtins__": __builtins__}
    try:
        exec(sol, g)
    except Exception as e:
        assert False, f"Execution error when loading candidate code: {e}"
        
    assert entry in g, f"Entry point '{entry}' not found in the executed namespace."
    assert callable(g[entry]), f"Entry point '{entry}' is not callable."

def test_signature_2():
    import builtins as _b
    import inspect
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    func = g[entry]
    
    try:
        sig = inspect.signature(func)
    except Exception as e:
        assert False, f"Could not inspect signature of {entry}: {e}"
        
    params = list(sig.parameters.values())
    assert len(params) == 2, f"Expected exactly 2 parameters, found {len(params)}."
    
    names = [p.name for p in params]
    assert 'circuit' in names or 'senders_basis' in names, f"Unexpected parameter names in signature: {names}"

def test_basic_plausibility_3():
    import builtins as _b
    from qiskit import QuantumCircuit
    import warnings
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    func = g[entry]
    
    qc = QuantumCircuit(1, 1)
    basis = [0]
    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            result = func(basis, qc)
        except Exception as e:
            assert False, f"Function '{entry}' raised an exception on a basic 1-qubit input: {e}"
            
    assert isinstance(result, str), f"Expected return type to be str, got {type(result).__name__}."