# SYNTACTIC tests — Qiskit HumanEval task task_0003
# Generated: 2026-04-28T12:39:35.690476
# Model: qwen/qwen3-coder-next (qwen3)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from qiskit.quantum_info import Statevector\n    import math\n    import matplotlib\n\n    def check_circuit(circuit):\n        assert circuit.data[-1].operation.name == "measure"\n        circuit.remove_final_measurements()\n        ghz_statevector = (\n            Statevector.from_label("000") + Statevector.from_label("111")\n        ) / math.sqrt(2)\n        assert Statevector.from_instruction(circuit).equiv(ghz_statevector)\n\n    circuit = candidate()\n    check_circuit(circuit)\n\n    circuit, drawing = candidate(drawing=True)\n    check_circuit(circuit)\n    assert isinstance(drawing, matplotlib.figure.Figure)\n'
ENTRY_POINT_NAME = 'create_ghz'
# --- Official check block end ---
import ast
import inspect
import builtins as _b

# Load solution and entry point from builtins
sol = _b.INJECTED_SOLUTION_CODE
entry = _b.INJECTED_ENTRY_POINT

# Parse and execute solution
tree = ast.parse(sol)
g = {"__builtins__": __builtins__}
exec(sol, g)

def test_module_loads_and_entry_exists():
    # Ensure the solution parses correctly and the entry point exists
    assert hasattr(g, '__builtins__'), "Module builtins missing"
    assert entry in g, f"Entry point '{entry}' not found in solution namespace"
    assert callable(g[entry]), f"Entry point '{entry}' is not callable"

def test_create_ghz_signature():
    # Check that create_ghz is callable and has correct parameter signature
    candidate = g[entry]
    sig = inspect.signature(candidate)
    params = list(sig.parameters.keys())
    assert 'drawing' in params, "Function 'create_ghz' must accept 'drawing' parameter"
    # Ensure default value for drawing is False
    drawing_param = sig.parameters['drawing']
    assert drawing_param.default is False, "Parameter 'drawing' must default to False"

def test_create_ghz_returns_quantumcircuit():
    # Test basic functionality: calling create_ghz() returns a QuantumCircuit
    from qiskit import QuantumCircuit
    candidate = g[entry]
    # Call without drawing argument
    circ = candidate()
    assert isinstance(circ, QuantumCircuit), "create_ghz() must return a QuantumCircuit instance"
    # Call with drawing=False explicitly
    circ2 = candidate(drawing=False)
    assert isinstance(circ2, QuantumCircuit), "create_ghz(drawing=False) must return a QuantumCircuit instance"