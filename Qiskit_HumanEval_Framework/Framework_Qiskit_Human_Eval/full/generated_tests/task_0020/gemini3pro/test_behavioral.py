# BEHAVIORAL tests — Qiskit HumanEval task task_0020
# Generated: 2026-04-28T12:02:12.761679
# Model: google/gemini-3.1-pro-preview (gemini3pro)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    result.remove_final_measurements()\n    backend = FakePerth()\n    assert result.num_qubits == backend.num_qubits\n    assert result.layout.initial_index_layout()[:3] == [2, 4, 6]\n'
ENTRY_POINT_NAME = 'transpile_ghz_customlayout'
# --- Official check block end ---
def test_transpile_ghz_customlayout_1():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    from qiskit import QuantumCircuit
    
    qc = candidate()
    
    assert isinstance(qc, QuantumCircuit), "Return value must be a QuantumCircuit."
    assert qc.num_qubits == 7, f"Expected exactly 7 qubits for FakePerth backend, but got {qc.num_qubits}."

def test_transpile_ghz_customlayout_2():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    qc = candidate()
    
    assert getattr(qc, "layout", None) is not None, "Transpiled circuit should have a layout attribute."
    assert getattr(qc.layout, "initial_layout", None) is not None, "Transpiled circuit should have an initial_layout."
    
    # Extract the mapping from virtual to physical qubits
    layout_dict = qc.layout.initial_layout.get_virtual_bits()
    
    mapped_physical_qubits = []
    for v_qubit, p_qubit in layout_dict.items():
        reg = getattr(v_qubit, "register", None)
        reg_name = reg.name.lower() if reg else ""
        # The transpiler typically adds an 'ancilla' register for unused physical qubits.
        # We filter those out to find the initial physical qubits assigned to the logical circuit.
        if 'ancilla' not in reg_name:
            mapped_physical_qubits.append(p_qubit)
            
    mapped_physical_qubits.sort()
    assert mapped_physical_qubits == [2, 4, 6], f"Expected initial layout to use physical qubits [2, 4, 6], got {mapped_physical_qubits}."

def test_transpile_ghz_customlayout_3():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    qc = candidate()
    
    try:
        from qiskit_ibm_runtime.fake_provider import FakePerth
    except ImportError:
        from qiskit.providers.fake_provider import FakePerth
        
    backend = FakePerth()
    basis_gates = set(backend.configuration().basis_gates)
    
    # The transpiler might preserve or add these non-gate instructions
    basis_gates.update(['measure', 'barrier', 'delay'])
    
    ops = qc.count_ops()
    for gate in ops:
        assert gate in basis_gates, f"Gate '{gate}' is not in the FakePerth basis gates: {basis_gates}"
        
    assert 'cx' in ops, "A transpiled GHZ state on FakePerth must contain 'cx' gates for entanglement."
    
    # A 3-qubit GHZ state requires at least 2 CX gates. Given the layout [2, 4, 6] on FakePerth,
    # the qubits are not directly connected, so SWAPs will be needed, resulting in even more CX gates.
    assert ops.get('cx', 0) >= 2, f"A 3-qubit GHZ state requires at least 2 CX gates, got {ops.get('cx', 0)}."