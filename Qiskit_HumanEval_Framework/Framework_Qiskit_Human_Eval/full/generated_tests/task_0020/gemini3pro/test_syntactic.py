# SYNTACTIC tests — Qiskit HumanEval task task_0020
# Generated: 2026-04-28T11:52:28.586207
# Model: google/gemini-3.1-pro-preview (gemini3pro)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    result.remove_final_measurements()\n    backend = FakePerth()\n    assert result.num_qubits == backend.num_qubits\n    assert result.layout.initial_index_layout()[:3] == [2, 4, 6]\n'
ENTRY_POINT_NAME = 'transpile_ghz_customlayout'
# --- Official check block end ---
def test_ast_parse_and_exec_1():
    import builtins as _b
    import ast
    
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    
    try:
        ast.parse(sol)
    except SyntaxError as e:
        assert False, f"SyntaxError in candidate solution: {e}"
        
    g = {"__builtins__": __builtins__}
    try:
        exec(sol, g)
    except Exception as e:
        assert False, f"Exception during execution of solution: {e}"
        
    assert entry in g, f"Entry point '{entry}' not found in the loaded namespace."
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
    
    assert len(sig.parameters) == 0, f"Expected 0 parameters in signature, got {len(sig.parameters)}."
    
    # Check if a return annotation is provided and looks like QuantumCircuit
    if sig.return_annotation != inspect.Signature.empty:
        ann_str = str(sig.return_annotation)
        assert "QuantumCircuit" in ann_str, f"Expected return annotation to mention QuantumCircuit, got {ann_str}"

def test_return_type_and_qubits_3():
    import builtins as _b
    from qiskit import QuantumCircuit
    
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    try:
        circuit = candidate()
    except Exception as e:
        assert False, f"Calling the candidate function raised an exception: {e}"
        
    assert isinstance(circuit, QuantumCircuit), f"Expected function to return a QuantumCircuit, got {type(circuit)}."
    
    # FakePerth is a 7-qubit backend, so the transpiled circuit mapped to it should have exactly 7 qubits
    assert circuit.num_qubits == 7, f"Expected transpiled circuit to have 7 qubits (FakePerth), got {circuit.num_qubits}."