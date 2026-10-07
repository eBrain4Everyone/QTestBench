# SEMANTIC tests — Qiskit HumanEval task task_0020
# Generated: 2026-04-28T11:12:31.378465
# Model: anthropic/claude-opus-4-6 (claudeopus46)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    result.remove_final_measurements()\n    backend = FakePerth()\n    assert result.num_qubits == backend.num_qubits\n    assert result.layout.initial_index_layout()[:3] == [2, 4, 6]\n'
ENTRY_POINT_NAME = 'transpile_ghz_customlayout'
# --- Official check block end ---
import pytest

def test_transpile_ghz_customlayout_1():
    """Test that the returned circuit is a valid QuantumCircuit transpiled for FakePerth."""
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    from qiskit import QuantumCircuit
    from qiskit_ibm_runtime.fake_provider import FakePerth

    result = candidate()
    backend = FakePerth()

    assert isinstance(result, QuantumCircuit), "Return type must be a QuantumCircuit"
    # FakePerth has 7 qubits; transpiled circuit should operate on the full backend width
    assert result.num_qubits == backend.num_qubits, (
        f"Transpiled circuit should have {backend.num_qubits} qubits (full backend width), "
        f"got {result.num_qubits}"
    )


def test_transpile_ghz_customlayout_2():
    """Test that the transpiled circuit uses the custom initial layout [2, 4, 6]."""
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    result = candidate()

    # Check that the layout information is present and maps virtual qubits 0,1,2 to physical 2,4,6
    layout = result.layout
    assert layout is not None, "Transpiled circuit should have layout information"

    initial_layout = layout.initial_layout
    # The initial layout should map virtual qubits (from the original 3-qubit circuit) to physical qubits 2, 4, 6
    physical_bits = []
    # Get the virtual-to-physical mapping
    virt_to_phys = initial_layout.get_virtual_bits()
    # virt_to_phys maps Qubit -> int (physical index)
    # We need to find which physical qubits the original 3 virtual qubits map to
    # The original circuit has 3 qubits; after transpilation the circuit has 7 qubits
    # The layout maps original virtual qubits to physical positions
    
    # Extract physical qubit indices for the original 3 virtual qubits
    from qiskit.circuit import Qubit
    original_physical = []
    for vqubit, pindex in virt_to_phys.items():
        original_physical.append(pindex)
    
    # The physical qubits 2, 4, 6 should be in the mapped set
    expected_layout = {2, 4, 6}
    # From the initial_layout, get physical bits for the first 3 virtual qubits
    phys_to_virt = initial_layout.get_physical_bits()
    # phys_to_virt: int -> Qubit
    
    # The original input routing should place the 3 logical qubits on physical 2, 4, 6
    input_qubit_mapping = layout.initial_virtual_layout(filter_ancillas=True)
    mapped_physical = set()
    for vq, pq in input_qubit_mapping.get_virtual_bits().items():
        mapped_physical.add(pq)
    
    assert mapped_physical == expected_layout, (
        f"Initial layout should map to physical qubits {{2, 4, 6}}, got {mapped_physical}"
    )


def test_transpile_ghz_customlayout_3():
    """Test that the transpiled circuit is functionally equivalent to a 3-qubit GHZ state."""
    import builtins as _b
    import numpy as np
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Operator, Statevector

    result = candidate()

    # Build the original 3-qubit GHZ circuit
    ghz = QuantumCircuit(3)
    ghz.h(0)
    ghz.cx(0, 1)
    ghz.cx(1, 2)

    # The transpiled circuit acts on 7 qubits but should be equivalent on the relevant qubits.
    # Simulate both and compare the statevector on the relevant qubits (2, 4, 6)
    sv_transpiled = Statevector.from_instruction(result)
    
    # Trace out ancilla qubits (keep only qubits at positions 2, 4, 6 in the 7-qubit system)
    # In Qiskit, qubit ordering is little-endian; qubit indices in the circuit are 0..6
    dm_transpiled = sv_transpiled.to_operator()
    
    # Use the Statevector and partial trace to get the reduced state on qubits [2, 4, 6]
    from qiskit.quantum_info import partial_trace, DensityMatrix
    dm_full = DensityMatrix(sv_transpiled)
    # Trace out qubits that are NOT in {2, 4, 6}, i.e., trace out {0, 1, 3, 5}
    dm_reduced = partial_trace(dm_full, [0, 1, 3, 5])

    # Expected GHZ state: (|000> + |111>) / sqrt(2)
    ghz_sv = Statevector.from_instruction(ghz)
    dm_ghz = DensityMatrix(ghz_sv)

    # Compare density matrices up to global phase (density matrices are phase-invariant)
    assert np.allclose(dm_reduced.data, dm_ghz.data, atol=1e-4, rtol=1e-5), (
        "The reduced density matrix on qubits [2,4,6] should match the 3-qubit GHZ state"
    )