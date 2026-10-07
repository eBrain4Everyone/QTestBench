# SEMANTIC tests — Qiskit HumanEval task task_0063
# Generated: 2026-04-28T12:13:50.120186
# Model: google/gemini-3.1-pro-preview (gemini3pro)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from numpy.random import seed\n    seed(12345)\n    basis = [1, 0, 0, 1, 1]\n    circuit = QuantumCircuit(5)\n    circuit.x([3, 4])\n    circuit.h([0, 3, 4])\n    result = candidate(basis, circuit)\n    assert result == "1"\n'
ENTRY_POINT_NAME = 'bb84_circuit_generate_key'
# --- Official check block end ---
import builtins as _b

def test_all_ones_1():
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    from qiskit import QuantumCircuit
    import numpy as np
    
    n = 50
    senders_basis = [i % 2 for i in range(n)]
    
    circuit = QuantumCircuit(n)
    for i in range(n):
        circuit.x(i)
        if senders_basis[i] == 1:
            circuit.h(i)
            
    np.random.seed(42)
    key = candidate(senders_basis, circuit)
    
    assert isinstance(key, str), f"Expected string, got {type(key)}"
    key = key.replace(' ', '').strip()
    assert len(key) > 0, "Generated key should not be empty"
    assert set(key) == {'1'}, f"Since Alice sent all 1s, the key should only contain '1's if bases matched correctly (checks for endianness bugs too). Got {key}"

def test_all_zeros_2():
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    from qiskit import QuantumCircuit
    import numpy as np
    
    n = 50
    senders_basis = [(i + 1) % 2 for i in range(n)]
    
    circuit = QuantumCircuit(n)
    for i in range(n):
        if senders_basis[i] == 1:
            circuit.h(i)
            
    np.random.seed(123)
    key = candidate(senders_basis, circuit)
    
    assert isinstance(key, str), f"Expected string, got {type(key)}"
    key = key.replace(' ', '').strip()
    assert len(key) > 0, "Generated key should not be empty"
    assert set(key) == {'0'}, f"Since Alice sent all 0s, the key should only contain '0's. Got {key}"

def test_key_length_3():
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]
    
    from qiskit import QuantumCircuit
    import numpy as np
    
    n = 200
    senders_basis = [i % 2 for i in range(n)]
    
    circuit = QuantumCircuit(n)
    for i in range(n):
        if senders_basis[i] == 1:
            circuit.h(i)
            
    np.random.seed(777)
    key = candidate(senders_basis, circuit)
    
    assert isinstance(key, str), f"Expected string, got {type(key)}"
    key = key.replace(' ', '').strip()
    assert 60 <= len(key) <= 140, f"Expected key length around 100 for n=200, got {len(key)}. This ensures random basis filtering is applied."
    assert set(key) == {'0'}, f"Since Alice sent all 0s, the filtered key must be exclusively '0'. Got {set(key)}"