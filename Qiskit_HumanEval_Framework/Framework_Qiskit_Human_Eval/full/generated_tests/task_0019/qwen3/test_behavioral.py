# BEHAVIORAL tests — Qiskit HumanEval task task_0019
# Generated: 2026-04-28T12:40:40.270289
# Model: qwen/qwen3-coder-next (qwen3)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    result.remove_final_measurements()\n    backend = FakeTorontoV2()\n    # Check initial layout is not the trivial layout (this is very unlikely\n    # if transpiled with optimization level 3)\n    assert result.layout.initial_index_layout() != list(range(backend.num_qubits))\n    # Optimization level 3 should easily find circuits with depth < 200\n    assert result.depth() < 150\n'
ENTRY_POINT_NAME = 'transpile_circuit_maxopt'
# --- Official check block end ---
def test_transpile_circuit_maxopt_1():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    # Test basic properties: circuit should be transpiled, have correct number of qubits, and include measurements
    circ = candidate()
    assert isinstance(circ, QuantumCircuit), "transpile_circuit_maxopt must return a QuantumCircuit"
    assert circ.num_qubits == 11, "Transpiled circuit must have 11 qubits"
    # Check that there are measurements
    measured_qubits = [i for i, instr in enumerate(circ.data) if isinstance(instr.operation, type(QuantumCircuit.measure))]
    # Alternatively, check if there are any measure instructions
    has_measure = any(inst.operation.name == 'measure' for inst in circ.data)
    assert has_measure, "Transpiled circuit must include measurements"


def test_transpile_circuit_maxopt_2():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    # Test that the circuit can be executed on FakeTorontoV2 backend without error
    from qiskit import Aer
    from qiskit_ibm_runtime.fake_provider import FakeTorontoV2

    backend = FakeTorontoV2()
    circ = candidate()

    # Simulate with Aer
    aer_sim = Aer.get_backend('aer_simulator')
    # Set seed for reproducibility
    result = aer_sim.run(circ, seed_simulator=42, shots=100).result()
    counts = result.get_counts()

    # GHZ states typically have two dominant outcomes (all-0 and all-1)
    # Since the circuit is 11-qubit GHZ, we expect large counts for |0...0> and |1...1>
    all_zero = '0' * 11
    all_one = '1' * 11
    assert all_zero in counts or all_one in counts, "GHZ circuit should produce |0...0> or |1...1> as dominant states"
    # At least one of the two expected states should have significant count
    total_expected = counts.get(all_zero, 0) + counts.get(all_one, 0)
    assert total_expected >= 80, f"GHZ state should produce mostly |0...0> or |1...1>, got {total_expected}/100 counts"


def test_transpile_circuit_maxopt_3():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    # Test circuit is properly mapped to backend coupling map
    from qiskit_ibm_runtime.fake_provider import FakeTorontoV2
    from qiskit.transpiler import CouplingMap

    backend = FakeTorontoV2()
    coupling_map = backend.configuration().coupling_map
    target_coupling = CouplingMap(coupling_map)

    circ = candidate()

    # Check that each 2-qubit gate in the circuit respects the coupling map
    for inst in circ.data:
        op = inst.operation
        if len(inst.qubits) == 2 and op.name not in ['id', 'u1', 'u2', 'u3', 'rz', 'sx', 'x']:  # skip single-qubit gates
            q0 = circ.find_bit(inst.qubits[0]).index
            q1 = circ.find_bit(inst.qubits[1]).index
            pair = (q0, q1)
            # Check both directions since coupling map is undirected
            assert (pair in target_coupling) or ((pair[1], pair[0]) in target_coupling), \
                f"2-qubit gate between qubits {q0} and {q1} violates coupling map"