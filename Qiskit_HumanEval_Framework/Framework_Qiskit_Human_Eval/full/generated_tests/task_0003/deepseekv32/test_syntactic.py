# SYNTACTIC tests — Qiskit HumanEval task task_0003
# Generated: 2026-04-28T11:21:12.393138
# Model: deepseek/deepseek-v3.2 (deepseekv32)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from qiskit.quantum_info import Statevector\n    import math\n    import matplotlib\n\n    def check_circuit(circuit):\n        assert circuit.data[-1].operation.name == "measure"\n        circuit.remove_final_measurements()\n        ghz_statevector = (\n            Statevector.from_label("000") + Statevector.from_label("111")\n        ) / math.sqrt(2)\n        assert Statevector.from_instruction(circuit).equiv(ghz_statevector)\n\n    circuit = candidate()\n    check_circuit(circuit)\n\n    circuit, drawing = candidate(drawing=True)\n    check_circuit(circuit)\n    assert isinstance(drawing, matplotlib.figure.Figure)\n'
ENTRY_POINT_NAME = 'create_ghz'
# --- Official check block end ---
import builtins as _b
import pytest
import inspect

def test_entry_point_exists_1():
    """Check that the solution code can be parsed and executed, and the entry point exists."""
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    assert entry in g, f"Entry point '{entry}' not found in solution module."
    candidate = g[entry]
    assert callable(candidate), f"'{entry}' is not callable."
    # verify it's a function (or at least callable)
    assert inspect.isfunction(candidate) or inspect.ismethod(candidate) or hasattr(candidate, '__call__'), f"'{entry}' is not a function or callable."

def test_signature_and_return_type_2():
    """Check that the function signature is compatible with the problem statement and returns a QuantumCircuit (or tuple) when called."""
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    # inspect signature (optional parameter drawing)
    sig = inspect.signature(candidate)
    param_names = list(sig.parameters.keys())
    # drawing parameter should be present (positional or keyword)
    assert 'drawing' in param_names, f"Function {entry} must have a parameter named 'drawing'."
    # check default value is False
    assert sig.parameters['drawing'].default is False, f"Parameter 'drawing' should default to False."
    # call with drawing=False, ensure returns QuantumCircuit (or tuple if drawing=True)
    circuit = candidate(drawing=False)
    from qiskit import QuantumCircuit
    assert isinstance(circuit, QuantumCircuit), f"Function returned {type(circuit)} when drawing=False, expected QuantumCircuit."
    # basic structure: 3 qubits
    assert circuit.num_qubits == 3, f"Circuit should have 3 qubits, got {circuit.num_qubits}."
    # should have at least one measurement (problem states "measure it")
    assert any(gate[0].name == 'measure' for gate in circuit.data), f"Circuit should contain at least one measurement gate."

def test_drawing_flag_behavior_3():
    """Check that drawing=True returns a tuple (circuit, drawing) and drawing=False returns only circuit."""
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    # call with drawing=False
    result_no_draw = candidate(drawing=False)
    from qiskit import QuantumCircuit
    assert isinstance(result_no_draw, QuantumCircuit), f"drawing=False should return a QuantumCircuit, got {type(result_no_draw)}."
    # call with drawing=True
    result_draw = candidate(drawing=True)
    assert isinstance(result_draw, tuple), f"drawing=True should return a tuple, got {type(result_draw)}."
    assert len(result_draw) == 2, f"Tuple length should be 2, got {len(result_draw)}."
    circuit_part, drawing_part = result_draw
    assert isinstance(circuit_part, QuantumCircuit), f"First tuple element should be QuantumCircuit, got {type(circuit_part)}."
    # drawing_part is a matplotlib figure or axes; we just check it's not None
    assert drawing_part is not None, f"Drawing part should not be None."