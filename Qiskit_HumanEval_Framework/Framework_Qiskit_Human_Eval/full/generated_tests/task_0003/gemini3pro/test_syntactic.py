# SYNTACTIC tests — Qiskit HumanEval task task_0003
# Generated: 2026-04-28T11:44:44.422125
# Model: google/gemini-3.1-pro-preview (gemini3pro)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from qiskit.quantum_info import Statevector\n    import math\n    import matplotlib\n\n    def check_circuit(circuit):\n        assert circuit.data[-1].operation.name == "measure"\n        circuit.remove_final_measurements()\n        ghz_statevector = (\n            Statevector.from_label("000") + Statevector.from_label("111")\n        ) / math.sqrt(2)\n        assert Statevector.from_instruction(circuit).equiv(ghz_statevector)\n\n    circuit = candidate()\n    check_circuit(circuit)\n\n    circuit, drawing = candidate(drawing=True)\n    check_circuit(circuit)\n    assert isinstance(drawing, matplotlib.figure.Figure)\n'
ENTRY_POINT_NAME = 'create_ghz'
# --- Official check block end ---
def test_syntax_and_exec_1():
    import ast
    import builtins as _b
    
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
        assert False, f"Solution raised an exception upon import/exec: {e}"
        
    assert entry in g, f"Entry point {entry} not found in module namespace."

def test_signature_and_callable_2():
    import inspect
    import builtins as _b
    
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    assert callable(candidate), f"Entry point {entry} is not a callable function."
    
    sig = inspect.signature(candidate)
    assert "drawing" in sig.parameters, "The function must accept a 'drawing' parameter."

def test_return_type_and_structure_3():
    import qiskit
    import builtins as _b
    
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    result = candidate(drawing=False)
    assert isinstance(result, qiskit.QuantumCircuit), f"Expected a QuantumCircuit when drawing=False, got {type(result)}."
    assert result.num_qubits == 3, f"Expected exactly 3 qubits for GHZ state, got {result.num_qubits}."
    assert result.num_clbits >= 3, f"Expected at least 3 classical bits for measurement, got {result.num_clbits}."
    
    has_measure = any(instr.operation.name == 'measure' for instr in result.data)
    assert has_measure, "The circuit must contain measurement operations."