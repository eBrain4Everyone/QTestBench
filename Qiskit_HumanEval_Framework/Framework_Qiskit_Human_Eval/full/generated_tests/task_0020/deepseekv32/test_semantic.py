# SEMANTIC tests — Qiskit HumanEval task task_0020
# Generated: 2026-04-28T11:25:51.323189
# Model: deepseek/deepseek-v3.2 (deepseekv32)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    result.remove_final_measurements()\n    backend = FakePerth()\n    assert result.num_qubits == backend.num_qubits\n    assert result.layout.initial_index_layout()[:3] == [2, 4, 6]\n'
ENTRY_POINT_NAME = 'transpile_ghz_customlayout'
# --- Official check block end ---
import builtins as _b
import numpy as np
import pytest
from qiskit import QuantumCircuit
from qiskit_ibm_runtime.fake_provider import FakePerth
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.quantum_info import Statevector, Operator
from qiskit_aer import AerSimulator

sol = _b.INJECTED_SOLUTION_CODE
entry = _b.INJECTED_ENTRY_POINT
_g = {"__builtins__": __builtins__}
exec(sol, _g)
candidate = _g[entry]

def test_ghz_circuit_1():
    """Test that the transpiled circuit has the correct number of qubits and uses the custom initial layout [2,4,6]."""
    import builtins as _b
    import numpy as np
    from qiskit import QuantumCircuit
    from qiskit_ibm_runtime.fake_provider import FakePerth
    from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
    from qiskit.quantum_info import Statevector

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    _g = {"__builtins__": __builtins__}
    exec(sol, _g)
    candidate = _g[entry]

    result_circuit = candidate()
    assert isinstance(result_circuit, QuantumCircuit), f"Expected QuantumCircuit, got {type(result_circuit)}"
    # The original GHZ circuit has 3 qubits, but after mapping to FakePerth (7 qubits) the circuit should have 7 qubits.
    assert result_circuit.num_qubits == 7, f"Expected 7 qubits after mapping to backend, got {result_circuit.num_qubits}"
    # Check that the initial layout [2,4,6] is used: the transpiled circuit should have operations that involve qubits 2,4,6.
    # We can check that at least one operation (e.g., a gate) is applied to qubit 2,4,6.
    # Since the GHZ circuit creates entanglement, there should be gates on those qubits.
    # We'll verify that the circuit is not empty and that the used qubits include 2,4,6.
    used_qubits = set()
    for instr, qargs, _ in result_circuit.data:
        for q in qargs:
            used_qubits.add(q.index)
    # The used qubits should be a subset of {2,4,6} plus possibly ancillas due to swaps_ Actually, with custom layout,
    # the logical qubits 0,1,2 are mapped to physical qubits 2,4,6. So all operations should be on those three physical qubits
    # (unless swaps are inserted to satisfy connectivity). FakePerth's coupling map may require swaps.
    # So we cannot assert that only qubits 2,4,6 are used, but we can assert that qubits 2,4,6 are among the used qubits.
    assert {2,4,6}.issubset(used_qubits), f"Qubits 2,4,6 not all used in circuit. Used qubits: {used_qubits}"
    # Additionally, the circuit should produce a GHZ state on those three qubits (up to swaps).
    # We'll test that in a separate test.

def test_ghz_statevector_2():
    """Test that the transpiled circuit, when simulated, produces the GHZ state on logical qubits 0,1,2 (mapped to 2,4,6)."""
    import builtins as _b
    import numpy as np
    from qiskit import QuantumCircuit
    from qiskit_ibm_runtime.fake_provider import FakePerth
    from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
    from qiskit.quantum_info import Statevector, Operator
    from qiskit_aer import AerSimulator

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    _g = {"__builtins__": __builtins__}
    exec(sol, _g)
    candidate = _g[entry]

    result_circuit = candidate()
    # Create a simulator and get the statevector.
    sim = AerSimulator(method='statevector')
    # The circuit may have measurements; remove them for statevector simulation.
    circ_no_measure = result_circuit.remove_final_measurements(inplace=False)
    # Run simulation
    job = sim.run(circ_no_measure, shots=1)
    result = job.result()
    statevector = result.get_statevector(circ_no_measure)
    # The GHZ state on three qubits is (|000> + |111>)/sqrt(2).
    # However, due to the initial layout mapping, the logical qubits 0,1,2 are mapped to physical qubits 2,4,6.
    # So the statevector of the full 7-qubit system should have amplitude only on basis states where qubits 2,4,6 are all 0 or all 1.
    # Let's compute the expected statevector for 7 qubits with GHZ on qubits 2,4,6.
    expected = np.zeros(2**7, dtype=complex)
    # indices where qubits 2,4,6 are 0: bits at positions 2,4,6 are 0.
    # We'll iterate over all 7-bit strings and set amplitude 1/sqrt(2) for those with bits 2,4,6 all 0 or all 1.
    for i in range(2**7):
        # Extract bits at positions 2,4,6 (using little-endian: qubit 0 is LSB).
        bit2 = (i >> 2) & 1
        bit4 = (i >> 4) & 1
        bit6 = (i >> 6) & 1
        if (bit2 == 0 and bit4 == 0 and bit6 == 0) or (bit2 == 1 and bit4 == 1 and bit6 == 1):
            expected[i] = 1/np.sqrt(2)
    # The statevector may have a global phase difference. Compare up to global phase.
    # Compute inner product and check magnitude is 1.
    inner = np.vdot(expected, statevector)
    assert np.allclose(np.abs(inner), 1.0, atol=1e-4), f"Statevector does not match GHZ state on qubits 2,4,6. Inner product magnitude = {np.abs(inner)}"

def test_ghz_counts_3():
    """Test that sampling from the transpiled circuit yields only all-zeros and all-ones on qubits 2,4,6."""
    import builtins as _b
    import numpy as np
    from qiskit import QuantumCircuit
    from qiskit_ibm_runtime.fake_provider import FakePerth
    from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
    from qiskit_aer import AerSimulator

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    _g = {"__builtins__": __builtins__}
    exec(sol, _g)
    candidate = _g[entry]

    result_circuit = candidate()
    # Ensure the circuit has measurements (the transpiled circuit likely does).
    # If not, add measurements to all qubits.
    if result_circuit.num_clbits == 0:
        measured_circuit = result_circuit.copy()
        measured_circuit.measure_all()
    else:
        measured_circuit = result_circuit
    # Use AerSimulator with a fixed seed for reproducibility.
    sim = AerSimulator(seed_simulator=42)
    # Run with a moderate number of shots.
    shots = 1024
    job = sim.run(measured_circuit, shots=shots, seed_simulator=42)
    result = job.result()
    counts = result.get_counts()
    # Check that every measured bitstring (7 bits) has qubits 2,4,6 either all 0 or all 1.
    # In Qiskit bitstrings are big-endian: the leftmost bit is qubit 7 (highest index) and rightmost is qubit 0.
    # So for a 7-qubit circuit, the bitstring is q6 q5 q4 q3 q2 q1 q0.
    # We need to extract bits at positions 2,4,6 in physical qubit indexing (which matches the bitstring order_).
    # Actually, the bitstring order is most significant bit is qubit (n-1) down to qubit 0.
    # So for 7 qubits, indices: bitstring[0] = q6, bitstring[1] = q5, bitstring[2] = q4, bitstring[3] = q3, bitstring[4] = q2, bitstring[5] = q1, bitstring[6] = q0.
    # Therefore qubit 2 corresponds to bitstring[4], qubit 4 to bitstring[2], qubit 6 to bitstring[0].
    for bitstr, count in counts.items():
        # pad with leading zeros if necessary
        if len(bitstr) != 7:
            bitstr = bitstr.zfill(7)
        bit2 = int(bitstr[4])
        bit4 = int(bitstr[2])
        bit6 = int(bitstr[0])
        assert (bit2 == 0 and bit4 == 0 and bit6 == 0) or (bit2 == 1 and bit4 == 1 and bit6 == 1), \
            f"Measured bitstring {bitstr} does not have qubits 2,4,6 all 0 or all 1 (bits: 2={bit2},4={bit4},6={bit6})"
    # Additionally, the total counts should be roughly 50/50 between the two patterns (allow some statistical variation).
    # Sum counts for all-zeros pattern on qubits 2,4,6.
    zeros_count = 0
    ones_count = 0
    for bitstr, count in counts.items():
        if len(bitstr) != 7:
            bitstr = bitstr.zfill(7)
        bit2 = int(bitstr[4])
        bit4 = int(bitstr[2])
        bit6 = int(bitstr[0])
        if bit2 == 0 and bit4 == 0 and bit6 == 0:
            zeros_count += count
        else:
            ones_count += count
    total = zeros_count + ones_count
    assert total == shots, f"Total counts {total} does not match shots {shots}"
    # Check that both patterns appear (GHZ state should have both).
    assert zeros_count > 0, "No all-zeros pattern observed"
    assert ones_count > 0, "No all-ones pattern observed"
    # Ratio should be about 0.5 within tolerance.
    ratio_zeros = zeros_count / shots
    assert np.allclose(ratio_zeros, 0.5, atol=0.05), f"Ratio of all-zeros pattern is {ratio_zeros}, expected ~0.5"