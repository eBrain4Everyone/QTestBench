# SYNTACTIC tests — Qiskit HumanEval task task_0003
# Generated: 2026-04-28T11:10:26.975903
# Model: anthropic/claude-opus-4-6 (claudeopus46)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from qiskit.quantum_info import Statevector\n    import math\n    import matplotlib\n\n    def check_circuit(circuit):\n        assert circuit.data[-1].operation.name == "measure"\n        circuit.remove_final_measurements()\n        ghz_statevector = (\n            Statevector.from_label("000") + Statevector.from_label("111")\n        ) / math.sqrt(2)\n        assert Statevector.from_instruction(circuit).equiv(ghz_statevector)\n\n    circuit = candidate()\n    check_circuit(circuit)\n\n    circuit, drawing = candidate(drawing=True)\n    check_circuit(circuit)\n    assert isinstance(drawing, matplotlib.figure.Figure)\n'
ENTRY_POINT_NAME = 'create_ghz'
# --- Official check block end ---
import pytest

def test_module_loads_and_parses_1():
    """Test that the solution source code is valid Python and can be parsed/executed."""
    import builtins as _b
    import ast
    
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    
    # Check that the source parses as valid Python
    tree = ast.parse(sol)
    assert tree is not None, "ast.parse returned None; source is not valid Python"
    
    # Check that exec succeeds without error
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    assert entry in g, f"Entry point '{entry}' not found in executed module namespace"


def test_entry_point_exists_and_callable_2():
    """Test that create_ghz exists in the namespace and is callable."""
    import builtins as _b
    import inspect
    
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    
    candidate = g[entry]
    assert callable(candidate), f"'{entry}' is not callable"
    
    # Check signature accepts a 'drawing' parameter
    sig = inspect.signature(candidate)
    params = list(sig.parameters.keys())
    assert "drawing" in params, f"Expected 'drawing' parameter in signature, got {params}"
    
    # Check that 'drawing' has a default value (False)
    drawing_param = sig.parameters["drawing"]
    assert drawing_param.default is not inspect.Parameter.empty, \
        "'drawing' parameter should have a default value"
    assert drawing_param.default == False, \
        f"'drawing' default should be False, got {drawing_param.default}"


def test_returns_quantum_circuit_3():
    """Test that create_ghz() returns a QuantumCircuit with basic plausible structure."""
    import builtins as _b
    from qiskit import QuantumCircuit
    
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    
    candidate = g[entry]
    
    # Call without drawing
    result = candidate(drawing=False)
    assert isinstance(result, QuantumCircuit), \
        f"Expected QuantumCircuit when drawing=False, got {type(result)}"
    
    # Should have 3 qubits for a 3-qubit GHZ state
    assert result.num_qubits == 3, \
        f"Expected 3 qubits for GHZ state, got {result.num_qubits}"
    
    # Should have measurements (problem says "measure it")
    assert result.num_clbits >= 3, \
        f"Expected at least 3 classical bits for measurement, got {result.num_clbits}"
    
    # When drawing=True, should return a tuple of (circuit, figure)
    result_with_drawing = candidate(drawing=True)
    assert isinstance(result_with_drawing, tuple), \
        f"Expected tuple when drawing=True, got {type(result_with_drawing)}"
    assert len(result_with_drawing) == 2, \
        f"Expected tuple of length 2 when drawing=True, got length {len(result_with_drawing)}"
    assert isinstance(result_with_drawing[0], QuantumCircuit), \
        f"First element of tuple should be QuantumCircuit, got {type(result_with_drawing[0])}"