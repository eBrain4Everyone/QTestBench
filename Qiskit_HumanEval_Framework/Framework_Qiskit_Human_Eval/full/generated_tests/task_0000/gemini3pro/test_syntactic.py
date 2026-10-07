# SYNTACTIC tests — Qiskit HumanEval task task_0000
# Generated: 2026-04-28T11:36:18.036629
# Model: google/gemini-3.1-pro-preview (gemini3pro)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate(3)\n    assert isinstance(result, QuantumCircuit)\n    assert result.num_qubits == 3\n'
ENTRY_POINT_NAME = 'create_quantum_circuit'
# --- Official check block end ---
def test_ast_and_execution_1():
    import builtins as _b
    import ast
    sol = getattr(_b, "INJECTED_SOLUTION_CODE", "")
    entry = getattr(_b, "INJECTED_ENTRY_POINT", "")
    
    try:
        ast.parse(sol)
    except Exception as e:
        assert False, f"Failed to parse AST of solution: {e}"
        
    g = {"__builtins__": __builtins__}
    try:
        exec(sol, g)
    except Exception as e:
        assert False, f"Failed to execute solution code: {e}"
        
    assert entry in g, f"Entry point '{entry}' not found in the executed namespace"


def test_callable_and_signature_2():
    import builtins as _b
    import inspect
    sol = getattr(_b, "INJECTED_SOLUTION_CODE", "")
    entry = getattr(_b, "INJECTED_ENTRY_POINT", "")
    
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    assert callable(candidate), f"Entry point '{entry}' is not callable"
    
    sig = inspect.signature(candidate)
    assert len(sig.parameters) >= 1, f"Expected at least 1 parameter for {entry}, found {len(sig.parameters)}"


def test_return_type_and_basic_properties_3():
    import builtins as _b
    from qiskit import QuantumCircuit
    sol = getattr(_b, "INJECTED_SOLUTION_CODE", "")
    entry = getattr(_b, "INJECTED_ENTRY_POINT", "")
    
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    n_qubits = 4
    qc = candidate(n_qubits)
    
    assert isinstance(qc, QuantumCircuit), f"Expected returned object to be a QuantumCircuit, but got {type(qc)}"
    assert qc.num_qubits == n_qubits, f"Expected the circuit to have exactly {n_qubits} qubits, but it has {qc.num_qubits}"