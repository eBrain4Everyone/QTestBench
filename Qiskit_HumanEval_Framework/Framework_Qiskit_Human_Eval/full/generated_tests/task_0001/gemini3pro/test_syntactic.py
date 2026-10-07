# SYNTACTIC tests — Qiskit HumanEval task task_0001
# Generated: 2026-04-28T11:37:16.601118
# Model: google/gemini-3.1-pro-preview (gemini3pro)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    assert isinstance(result, dict)\n    assert result.keys() == {"00", "11"}\n    assert 0.4 < (result["00"] / sum(result.values())) < 0.6\n'
ENTRY_POINT_NAME = 'run_bell_state_simulator'
# --- Official check block end ---
def test_ast_parse_and_exec_1():
    import builtins as _b
    import ast
    
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    
    try:
        ast.parse(sol)
    except SyntaxError as e:
        raise AssertionError(f"SyntaxError in solution code: {e}")
        
    g = {"__builtins__": __builtins__}
    try:
        exec(sol, g)
    except Exception as e:
        raise AssertionError(f"Execution of solution code failed: {e}")
        
    assert entry in g, f"Entry point '{entry}' not found in executed namespace."
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
    
    assert len(sig.parameters) == 0, f"Expected 0 parameters for '{entry}', found {len(sig.parameters)}."

def test_imports_in_source_3():
    import builtins as _b
    import ast
    
    sol = _b.INJECTED_SOLUTION_CODE
    
    try:
        tree = ast.parse(sol)
    except Exception:
        return  # test_ast_parse_and_exec_1 handles syntax errors
    
    has_qiskit_import = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if 'qiskit' in alias.name:
                    has_qiskit_import = True
                    break
        elif isinstance(node, ast.ImportFrom):
            if node.module and 'qiskit' in node.module:
                has_qiskit_import = True
                break
                
    assert has_qiskit_import, "The solution does not appear to import from 'qiskit', which is required for this task."