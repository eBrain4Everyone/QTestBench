# BEHAVIORAL tests — Qiskit HumanEval task task_0063
# Generated: 2026-04-28T12:26:11.037271
# Model: google/gemini-3.1-pro-preview (gemini3pro)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from numpy.random import seed\n    seed(12345)\n    basis = [1, 0, 0, 1, 1]\n    circuit = QuantumCircuit(5)\n    circuit.x([3, 4])\n    circuit.h([0, 3, 4])\n    result = candidate(basis, circuit)\n    assert result == "1"\n'
ENTRY_POINT_NAME = 'bb84_circuit_generate_key'
# --- Official check block end ---
def test_bb84_all_zeros_1():
    import builtins as _b
    from qiskit import QuantumCircuit
    import numpy as np
    import random
    
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    func = g[entry]

    n = 60
    # Asymmetric bases to reliably catch Qiskit endianness extraction bugs
    bases = [0 if i % 3 == 0 else 1 for i in range(n)]
    qc = QuantumCircuit(n, n)
    
    # Alice prepares all 0s
    for i in range(n):
        if bases[i] == 1:
            qc.h(i)
            
    np.random.seed(123)
    random.seed(123)
    key = func(bases, qc)
    
    assert isinstance(key, str), f"Expected string, got {type(key)}"
    assert len(key) > 0, "Key should not be empty"
    assert all(bit == '0' for bit in key), f"Expected all zeros in key, got {key}. Check endianness and basis matching."

def test_bb84_all_ones_2():
    import builtins as _b
    from qiskit import QuantumCircuit
    import numpy as np
    import random
    
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    func = g[entry]

    n = 60
    # Asymmetric bases to reliably catch Qiskit endianness extraction bugs
    bases = [1 if i % 4 == 0 else 0 for i in range(n)]
    qc = QuantumCircuit(n, n)
    
    # Alice prepares all 1s
    for i in range(n):
        qc.x(i)
        if bases[i] == 1:
            qc.h(i)
            
    np.random.seed(456)
    random.seed(456)
    key = func(bases, qc)
    
    assert isinstance(key, str), f"Expected string, got {type(key)}"
    assert len(key) > 0, "Key should not be empty"
    assert all(bit == '1' for bit in key), f"Expected all ones in key, got {key}. Check endianness and basis matching."

def test_bb84_filtering_3():
    import builtins as _b
    from qiskit import QuantumCircuit
    import numpy as np
    import random
    
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    func = g[entry]

    n = 100
    np.random.seed(42)
    random.seed(42)
    
    # Random Alice bits and bases
    bases = np.random.randint(0, 2, n).tolist()
    bits = np.random.randint(0, 2, n).tolist()
    
    qc = QuantumCircuit(n, n)
    for i in range(n):
        if bits[i] == 1:
            qc.x(i)
        if bases[i] == 1:
            qc.h(i)
            
    key = func(bases, qc)
    
    assert isinstance(key, str), f"Expected string, got {type(key)}"
    # The key length should be roughly n/2 (Binomial distribution with p=0.5).
    # Bounds of 20 to 80 represent +/- 6 standard deviations, practically impossible to fail if correct.
    assert 20 < len(key) < 80, f"Expected key length roughly half of {n}, got {len(key)}. Basis filtering might be missing."