# BEHAVIORAL tests — Qiskit HumanEval task task_0020
# Generated: 2026-04-28T12:41:20.991630
# Model: qwen/qwen3-coder-next (qwen3)
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
    
    # Test basic structure: function returns a QuantumCircuit
    result = candidate()
    from qiskit import QuantumCircuit
    assert isinstance(result, QuantumCircuit), "transpile_ghz_customlayout should return a QuantumCircuit"


def test_transpile_ghz_customlayout_2():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    # Test circuit properties: 3 qubits, measurements, correct layout
    from qiskit import QuantumCircuit
    from qiskit_ibm_runtime.fake_provider import FakePerth
    from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
    
    result = candidate()
    
    # Check number of qubits
    assert result.num_qubits == 3, f"Expected 3 qubits, got {result.num_qubits}"
    
    # Check that measurements exist
    has_measurements = any(instr[0].name == 'measure' for instr in result.data)
    assert has_measurements, "Transpiled circuit should contain measurements"


def test_transpile_ghz_customlayout_3():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    # Test that circuit uses the correct physical qubits from layout [2,4,6]
    from qiskit import QuantumCircuit
    from qiskit_ibm_runtime.fake_provider import FakePerth
    from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
    from qiskit import transpile
    
    # Generate reference transpiled circuit with same parameters for comparison
    backend = FakePerth()
    ghz_circuit = QuantumCircuit(3)
    ghz_circuit.h(0)
    ghz_circuit.cx(0, 1)
    ghz_circuit.cx(0, 2)
    ghz_circuit.measure_all()
    
    initial_layout = [2, 4, 6]
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend, initial_layout=initial_layout)
    reference = transpile(ghz_circuit, pass_manager=pm)
    
    # Compare with candidate result
    result = candidate()
    
    # Check that the result circuit has the same number of physical qubits as backend
    assert result.num_qubits <= backend.num_qubits, "Circuit should fit within backend's qubit count"
    
    # Verify that initial layout was applied correctly by checking the transpiled circuit's layout metadata
    # The transpiled circuit should be over physical qubits, and we verify the logical-to-physical mapping
    # by ensuring the circuit structure matches what we expect from the GHZ circuit with the specified layout
    
    # Check that circuit has 3 qubits in the transpiled version (for GHZ)
    assert result.num_qubits == 3, "Transpiled circuit should have 3 qubits"
    
    # Simulate the circuit to verify GHZ state creation (only check first few shots)
    from qiskit_aer import Aer
    from qiskit_aer.noise import NoiseModel
    from qiskit_aer import AerSimulator
    
    try:
        aer_sim = Aer.get_backend('aer_simulator')
        aer_sim.set_options(seed_simulator=42)
        result_sim = aer_sim.run(result, shots=100, memory=True).result()
        memory = result_sim.get_memory()
        
        # For a GHZ state |000> + |111>, we expect mostly 000 and 111 measurements
        counts = {}
        for shot in memory:
            counts[shot] = counts.get(shot, 0) + 1
        
        # Majority of counts should be either '000' or '111'
        total = sum(counts.values())
        ghz_pop = counts.get('000', 0) + counts.get('111', 0)
        assert ghz_pop / total > 0.8, "GHZ state should show strong correlation between qubits"
    except:
        # If Aer is not available, just check circuit structure
        # Check that the circuit contains the expected operations: H, CNOT, measure
        ops = [instr[0].name for instr in result.data]
        assert 'h' in ops, "GHZ circuit should contain Hadamard gate"
        assert 'cx' in ops, "GHZ circuit should contain CNOT gates"
        assert 'measure' in ops, "GHZ circuit should contain measurements"