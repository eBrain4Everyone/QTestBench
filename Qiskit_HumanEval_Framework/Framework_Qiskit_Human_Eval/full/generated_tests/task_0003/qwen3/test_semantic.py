# SEMANTIC tests — Qiskit HumanEval task task_0003
# Generated: 2026-04-28T12:39:54.021881
# Model: qwen/qwen3-coder-next (qwen3)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from qiskit.quantum_info import Statevector\n    import math\n    import matplotlib\n\n    def check_circuit(circuit):\n        assert circuit.data[-1].operation.name == "measure"\n        circuit.remove_final_measurements()\n        ghz_statevector = (\n            Statevector.from_label("000") + Statevector.from_label("111")\n        ) / math.sqrt(2)\n        assert Statevector.from_instruction(circuit).equiv(ghz_statevector)\n\n    circuit = candidate()\n    check_circuit(circuit)\n\n    circuit, drawing = candidate(drawing=True)\n    check_circuit(circuit)\n    assert isinstance(drawing, matplotlib.figure.Figure)\n'
ENTRY_POINT_NAME = 'create_ghz'
# --- Official check block end ---
def test_create_ghz_basic_structure():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    # Test basic circuit creation without drawing
    circuit = candidate(drawing=False)
    
    # Check it's a QuantumCircuit
    from qiskit import QuantumCircuit
    assert isinstance(circuit, QuantumCircuit), "Function should return a QuantumCircuit"
    
    # Check it has exactly 3 qubits and 3 classical bits (for measurement)
    assert circuit.num_qubits == 3, "GHZ state should be created on 3 qubits"
    assert circuit.num_clbits == 3, "GHZ state should be measured on 3 classical bits"
    
    # Check gates: should have H on qubit 0, CNOTs from qubit 0 to 1 and 2, and measurements
    ops = circuit.data
    gate_names = [op[0].name for op in ops]
    
    # Verify presence of required operations
    assert 'h' in gate_names, "Should apply Hadamard gate"
    assert 'cx' in gate_names, "Should apply CNOT gates"
    assert 'measure' in gate_names, "Should apply measurements"
    
    # Check measurement is on all qubits
    measurement_ops = [op for op in ops if op[0].name == 'measure']
    assert len(measurement_ops) == 3, "Should measure all 3 qubits"


def test_create_ghz_state_vector():
    import builtins as _b
    import numpy as np
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    # Get circuit
    circuit = candidate(drawing=False)
    
    # Simulate to get statevector
    from qiskit.quantum_info import Statevector
    state = Statevector.from_instruction(circuit)
    
    # GHZ state should be (|000_ + |111_)/_2 up to global phase
    expected = np.array([1/np.sqrt(2), 0, 0, 0, 0, 0, 0, 1/np.sqrt(2)])
    
    # Compare up to global phase
    # Check if state is proportional to expected
    ratio1 = state[0] / expected[0] if expected[0] != 0 else 0
    ratio8 = state[7] / expected[7] if expected[7] != 0 else 0
    
    # All non-zero amplitudes should have same ratio (same global phase)
    assert np.allclose(ratio1, ratio8, atol=1e-4), "State should have equal amplitudes for |000_ and |111_"
    
    # All other amplitudes should be ~0
    for i in [1, 2, 3, 4, 5, 6]:
        assert np.abs(state[i]) < 1e-5, f"Amplitude for |{i:03b}_ should be ~0"


def test_create_ghz_measurement_distribution():
    import builtins as _b
    import numpy as np
    from qiskit import Aer, execute
    
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    # Get circuit
    circuit = candidate(drawing=False)
    
    # Simulate with Aer
    simulator = Aer.get_backend('qasm_simulator')
    result = execute(circuit, simulator, shots=1000, seed_simulator=42).result()
    counts = result.get_counts()
    
    # GHZ state should yield only |000_ and |111_ with roughly equal probability
    assert '000' in counts, "Should measure |000_"
    assert '111' in counts, "Should measure |111_"
    
    # Check no other outcomes (within statistical tolerance)
    other_outcomes = [k for k in counts.keys() if k not in ['000', '111']]
    assert len(other_outcomes) == 0, "GHZ state should not produce other measurement outcomes"
    
    # Check probabilities are roughly equal (000 and 111 should each be ~50%)
    prob_000 = counts['000'] / 1000
    prob_111 = counts['111'] / 1000
    assert np.abs(prob_000 - 0.5) < 0.05, "Probability of |000_ should be ~50%"
    assert np.abs(prob_111 - 0.5) < 0.05, "Probability of |111_ should be ~50%"


def test_create_ghz_drawing_parameter():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    # Test with drawing=False
    result_no_draw = candidate(drawing=False)
    from qiskit import QuantumCircuit
    assert isinstance(result_no_draw, QuantumCircuit), "Should return circuit when drawing=False"
    
    # Test with drawing=True (should return a tuple)
    result_with_draw = candidate(drawing=True)
    assert isinstance(result_with_draw, tuple), "Should return tuple when drawing=True"
    assert len(result_with_draw) == 2, "Should return (circuit, drawing) when drawing=True"
    
    circuit, drawing = result_with_draw
    assert isinstance(circuit, QuantumCircuit), "First element should be circuit"
    # Matplotlib drawing is usually an Axes object or similar
    try:
        import matplotlib
        assert hasattr(drawing, 'get_figure') or hasattr(drawing, 'axes'), "Second element should be a drawing object"
    except ImportError:
        # If matplotlib not available, just check it's not None
        assert drawing is not None, "Drawing should not be None"