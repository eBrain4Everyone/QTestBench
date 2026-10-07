# SEMANTIC tests — Qiskit HumanEval task task_0019
# Generated: 2026-04-28T11:50:19.818646
# Model: google/gemini-3.1-pro-preview (gemini3pro)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    result = candidate()\n    result.remove_final_measurements()\n    backend = FakeTorontoV2()\n    # Check initial layout is not the trivial layout (this is very unlikely\n    # if transpiled with optimization level 3)\n    assert result.layout.initial_index_layout() != list(range(backend.num_qubits))\n    # Optimization level 3 should easily find circuits with depth < 200\n    assert result.depth() < 150\n'
ENTRY_POINT_NAME = 'transpile_circuit_maxopt'
# --- Official check block end ---
def test_transpile_circuit_maxopt_1():
    import builtins as _b
    from qiskit import QuantumCircuit
    
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    circ = candidate()
    
    assert isinstance(circ, QuantumCircuit), "Return value must be a QuantumCircuit."
    assert circ.num_qubits == 27, f"Expected exactly 27 qubits for the mapped FakeTorontoV2 backend, got {circ.num_qubits}."
    
    # FakeTorontoV2 basis gates
    valid_bases = {'id', 'rz', 'sx', 'x', 'cx', 'reset', 'measure', 'delay', 'barrier'}
    circ_bases = set(circ.count_ops().keys())
    invalid_gates = circ_bases - valid_bases
    assert not invalid_gates, f"Transpiled circuit contains invalid gates for the target backend: {invalid_gates}"


def test_transpile_circuit_maxopt_2():
    import builtins as _b
    from qiskit import QuantumCircuit
    
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    circ = candidate()
    
    # Find all physical qubits that have operations applied (excluding idle/delay)
    active_qubits = set()
    for inst in circ.data:
        if inst.operation.name not in ['barrier', 'delay', 'measure']:
            for q in inst.qubits:
                active_qubits.add(circ.find_bit(q).index)
                
    assert len(active_qubits) >= 11, f"Expected at least 11 active qubits for an 11-qubit GHZ state, got {len(active_qubits)}."
    
    ops = circ.count_ops()
    assert 'cx' in ops, "Circuit must contain 'cx' gates to generate entanglement."
    assert ops['cx'] >= 10, f"An 11-qubit GHZ state requires at least 10 'cx' gates, got {ops.get('cx', 0)}."


def test_transpile_circuit_maxopt_3():
    import builtins as _b
    from qiskit_aer import AerSimulator
    from qiskit import QuantumCircuit
    from qiskit.circuit import ClassicalRegister
    
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    circ = candidate()
    
    # Identify all active Qubit objects to measure
    active_qubits = set()
    for inst in circ.data:
        if inst.operation.name not in ['barrier', 'delay', 'measure']:
            for q in inst.qubits:
                active_qubits.add(q)
    active_qubits = list(active_qubits)
    
    assert len(active_qubits) >= 11, "Circuit does not have enough active qubits to represent the GHZ state."
    
    # Build a clean state preparation circuit without existing measurements/delays
    clean_circ = QuantumCircuit(*circ.qregs)
    for inst in circ.data:
        if inst.operation.name not in ['delay', 'barrier', 'measure']:
            clean_circ.append(inst.operation, inst.qubits)
            
    # Measure all active physical qubits into a new classical register
    cr = ClassicalRegister(len(active_qubits))
    clean_circ.add_register(cr)
    clean_circ.measure(active_qubits, cr)
        
    # Simulate the transpiled circuit precisely via MPS (ideal for GHZ state structure)
    sim = AerSimulator(method='matrix_product_state')
    res = sim.run(clean_circ, shots=1024, seed_simulator=42).result()
    counts = res.get_counts()
    
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    
    assert len(sorted_counts) >= 2, "A GHZ state should yield at least two distinct measurement outcomes."
    assert sorted_counts[0][1] > 300, f"The dominant bitstring probability is too low ({sorted_counts[0][1]} shots)."
    assert sorted_counts[1][1] > 300, f"The second dominant bitstring probability is too low ({sorted_counts[1][1]} shots)."
    
    bs1 = sorted_counts[0][0].replace(' ', '')
    bs2 = sorted_counts[1][0].replace(' ', '')
    
    # Regardless of SWAPs and mapping, the two dominant branches of an 11-qubit GHZ state 
    # must differ in exactly 11 positions. Inactive or intermediate SWAP qubits will remain identical (|0>).
    hamming_dist = sum(1 for a, b in zip(bs1, bs2) if a != b)
    assert hamming_dist == 11, f"Expected the two GHZ branches to differ by exactly 11 bits, got a distance of {hamming_dist}."