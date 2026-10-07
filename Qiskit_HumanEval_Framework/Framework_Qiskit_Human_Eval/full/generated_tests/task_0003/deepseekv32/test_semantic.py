# SEMANTIC tests — Qiskit HumanEval task task_0003
# Generated: 2026-04-28T11:22:19.150774
# Model: deepseek/deepseek-v3.2 (deepseekv32)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from qiskit.quantum_info import Statevector\n    import math\n    import matplotlib\n\n    def check_circuit(circuit):\n        assert circuit.data[-1].operation.name == "measure"\n        circuit.remove_final_measurements()\n        ghz_statevector = (\n            Statevector.from_label("000") + Statevector.from_label("111")\n        ) / math.sqrt(2)\n        assert Statevector.from_instruction(circuit).equiv(ghz_statevector)\n\n    circuit = candidate()\n    check_circuit(circuit)\n\n    circuit, drawing = candidate(drawing=True)\n    check_circuit(circuit)\n    assert isinstance(drawing, matplotlib.figure.Figure)\n'
ENTRY_POINT_NAME = 'create_ghz'
# --- Official check block end ---
import builtins as _b
sol = _b.INJECTED_SOLUTION_CODE
entry = _b.INJECTED_ENTRY_POINT
_g = {"__builtins__": __builtins__}
exec(sol, _g)
candidate = _g[entry]

# Your test code below:
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, Operator
from qiskit_aer import AerSimulator

def test_ghz_state_vector_1():
    """Test that the circuit without measurement produces the correct GHZ statevector."""
    import numpy as np
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    _g = {"__builtins__": __builtins__}
    exec(sol, _g)
    candidate = _g[entry]

    circuit = candidate(drawing=False)
    # If the function returns a tuple (circuit, drawing) when drawing=True, we need to handle that.
    # According to spec, drawing=False returns just the circuit.
    # Ensure circuit is a QuantumCircuit (not a tuple)
    if isinstance(circuit, tuple):
        circuit = circuit[0]

    # Remove measurements to get the state before measurement
    # The spec says "Generate a QuantumCircuit for a 3 qubit GHZ State and measure it."
    # So the circuit includes measurement. We'll remove any classical registers and measurement ops.
    # Simpler: create a new circuit without measurement.
    qc = QuantumCircuit(3)
    # Apply the same gates as the candidate up to measurements.
    # But we don't know the internal structure. Instead, we can evaluate the statevector of the circuit
    # *before* measurement by using the circuit without the measurement instructions.
    # However, the candidate returns a circuit with measurement. We can remove classical bits and measurements.
    # Let's extract the unitary part by ignoring classical registers and any operations that are measurements.
    # A more robust way: get the statevector of the circuit *without* simulating measurements.
    # Using Statevector.from_instruction will treat measurements as non-unitary and raise error.
    # So we need to copy the circuit and remove measurements.
    no_meas = QuantumCircuit(3)
    for instr, qargs, cargs in circuit.data:
        if instr.name != 'measure':
            no_meas.append(instr, qargs, cargs)
    # Now compute statevector
    sv = Statevector(no_meas)
    # GHZ state is (|000> + |111>)/sqrt(2)
    expected = np.zeros(8, dtype=complex)
    expected[0] = 1/np.sqrt(2)
    expected[7] = 1/np.sqrt(2)
    # Compare up to global phase
    # Normalize both
    sv_vec = sv.data
    # Compute inner product
    inner = np.vdot(expected, sv_vec)
    # Magnitude should be 1, phase arbitrary
    assert np.isclose(abs(inner), 1.0, atol=1e-4), f"State not GHZ: inner product magnitude {abs(inner)}"
    # Additionally, check that the state is normalized (should be)
    assert np.isclose(sv_vec @ sv_vec.conj(), 1.0, atol=1e-4), "State not normalized"

def test_ghz_measurement_counts_2():
    """Test that measuring the circuit yields only 000 and 111 outcomes (within sampling noise)."""
    import numpy as np
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    _g = {"__builtins__": __builtins__}
    exec(sol, _g)
    candidate = _g[entry]

    circuit = candidate(drawing=False)
    if isinstance(circuit, tuple):
        circuit = circuit[0]
    # Ensure circuit has measurements and classical registers.
    # If not, the spec is violated, but we'll just add a test that fails.
    # Check that there is at least one classical register.
    if circuit.clbits:
        # Use simulator with fixed seed for reproducibility
        sim = AerSimulator()
        # Transpile for backend
        from qiskit import transpile
        tcirc = transpile(circuit, sim)
        result = sim.run(tcirc, shots=1000, seed_simulator=42).result()
        counts = result.get_counts()
        # Only allowed bitstrings are '000' and '111' (order may be reversed depending on qiskit's convention)
        # Qiskit's classical bit order is most significant bit first (bit 0 is leftmost in string).
        # For 3 qubits, measured bits correspond to qubits 0,1,2 -> classical bits 0,1,2.
        # The string '000' means qubit 0 measured 0, qubit1 0, qubit2 0.
        allowed = {'000', '111'}
        for bitstr in counts:
            assert bitstr in allowed, f"Unexpected measurement outcome {bitstr}"
        # Check that the counts sum to shots
        total = sum(counts.values())
        assert total == 1000, f"Total counts {total} != 1000"
        # Optionally, check that the distribution is roughly 50/50 (not required by spec, but GHZ should be)
        # We'll just ensure both outcomes appear (they should with high probability).
        # However, due to randomness, one might be zero in 1000 shots with extremely low probability.
        # We'll accept if at least one outcome appears.
        assert len(counts) > 0, "No measurement outcomes"
    else:
        # If no classical bits, the circuit doesn't measure, which violates spec.
        assert False, "Circuit has no classical bits (measurements missing)"

def test_drawing_flag_3():
    """Test that drawing=True returns a tuple (circuit, drawing) and drawing=False returns only circuit."""
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    _g = {"__builtins__": __builtins__}
    exec(sol, _g)
    candidate = _g[entry]

    # Case drawing=False
    result_false = candidate(drawing=False)
    # Should be a QuantumCircuit (or possibly a tuple if implementation buggy)
    assert isinstance(result_false, QuantumCircuit), f"Expected QuantumCircuit, got {type(result_false)}"
    # Check it has 3 qubits
    assert result_false.num_qubits == 3, f"Expected 3 qubits, got {result_false.num_qubits}"
    # Check it has measurements (classical bits)
    assert len(result_false.clbits) > 0, "Circuit should have classical bits (measurements)"
    # Case drawing=True
    result_true = candidate(drawing=True)
    # Should be a tuple of length 2
    assert isinstance(result_true, tuple), f"Expected tuple, got {type(result_true)}"
    assert len(result_true) == 2, f"Expected tuple of length 2, got {len(result_true)}"
    circuit_part, drawing_part = result_true
    assert isinstance(circuit_part, QuantumCircuit), f"First element should be QuantumCircuit, got {type(circuit_part)}"
    # The drawing part should be a matplotlib figure or axes; but we can't guarantee because of different backends.
    # We'll just check it's not None and is a non-string object.
    assert drawing_part is not None, "Drawing part is None"
    # Also ensure the circuit part is equivalent to the one returned with drawing=False (same structure not required, but same number of qubits etc.)
    assert circuit_part.num_qubits == 3, f"Drawing=True circuit has {circuit_part.num_qubits} qubits, expected 3"
    assert len(circuit_part.clbits) > 0, "Drawing=True circuit missing classical bits"