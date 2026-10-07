# SYNTACTIC tests — Qiskit HumanEval task task_0034
# Generated: 2026-04-28T12:04:28.156454
# Model: google/gemini-3.1-pro-preview (gemini3pro)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = "def check(candidate):\n    from numpy import isclose\n    jobs = candidate()\n    reference_data = {\n        'phi_plus': {'00': 0.10, '11': 0.10},\n        'phi_minus': {'00': 0.10, '11': 0.10},\n        'psi_plus': {'01': 0.10, '10': 0.10},\n        'psi_minus': {'01': 0.1, '10': 0.10}\n    }\n    assert isinstance(jobs, dict)\n    assert set(jobs.keys()) == set(reference_data.keys())\n    for state, job in jobs.items():\n        assert isinstance(job, PrimitiveJob)\n        assert job.job_id() is not None\n        counts = job.result()[0].data.meas.get_counts()\n        shots = 4096\n        normalized_counts = {k: v/shots for k, v in counts.items()}\n        for key, value in reference_data[state].items():\n            assert isclose(normalized_counts[key], value, atol=1e-01)\n"
ENTRY_POINT_NAME = 'run_jobs_on_batch'
# --- Official check block end ---
def test_ast_parse_and_callable_1():
    import builtins as _b
    import ast
    
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    
    try:
        ast.parse(sol)
    except SyntaxError as e:
        assert False, f"Solution code has syntax error: {e}"
        
    g = {"__builtins__": __builtins__}
    try:
        exec(sol, g)
    except Exception as e:
        assert False, f"Solution code failed to execute top-level: {e}"
        
    assert entry in g, f"Entry point '{entry}' not found."
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
    
    assert len(sig.parameters) == 0, f"Expected 0 parameters, got {len(sig.parameters)}."
    
    ret_ann = sig.return_annotation
    if ret_ann != inspect.Signature.empty:
        ann_str = str(ret_ann).lower()
        assert 'dict' in ann_str, f"Expected return annotation to indicate dict, got {ret_ann}"

def test_source_code_keywords_3():
    import builtins as _b
    import ast
    
    sol = _b.INJECTED_SOLUTION_CODE
    
    try:
        tree = ast.parse(sol)
    except SyntaxError:
        return 
        
    found_names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            found_names.add(node.id)
        elif isinstance(node, ast.alias):
            found_names.add(node.name)
            if node.asname:
                found_names.add(node.asname)
        elif isinstance(node, ast.Attribute):
            found_names.add(node.attr)
            
    required_keywords = ['FakeAlgiers', 'Batch', 'QuantumCircuit']
    for kw in required_keywords:
        assert kw in found_names, f"Expected keyword '{kw}' to be present in the source code."