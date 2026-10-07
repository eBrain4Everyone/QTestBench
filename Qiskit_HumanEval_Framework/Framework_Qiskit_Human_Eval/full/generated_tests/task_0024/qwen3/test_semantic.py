# SEMANTIC tests — Qiskit HumanEval task task_0024
# Generated: 2026-04-28T12:41:32.154988
# Model: qwen/qwen3-coder-next (qwen3)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    balanced = QuantumCircuit(5)\n    balanced.cx(3, 4)\n    assert candidate(balanced) == False\n    constant = QuantumCircuit(9)\n    constant.x(8)\n    assert candidate(constant) == True\n'
ENTRY_POINT_NAME = 'dj_algorithm'
# --- Official check block end ---
def test_dj_algorithm_constant_oracle_1():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    from qiskit import QuantumCircuit
    import numpy as np
    
    # Create a constant oracle (always outputs 0)
    n = 3
    qc = QuantumCircuit(n + 1)
    # Identity on first n qubits, do nothing on last qubit (constant 0)
    # This represents f(x) = 0 for all x
    
    result = candidate(qc)
    assert result is True, "Constant oracle (f(x)=0) should return True"


def test_dj_algorithm_constant_oracle_2():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    from qiskit import QuantumCircuit
    import numpy as np
    
    # Create a constant oracle (always outputs 1)
    n = 2
    qc = QuantumCircuit(n + 1)
    # Apply X gate to the last qubit to flip it (f(x) = 1 for all x)
    qc.x(n)
    
    result = candidate(qc)
    assert result is True, "Constant oracle (f(x)=1) should return True"


def test_dj_algorithm_balanced_oracle():
    import builtins as _b
    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    from qiskit import QuantumCircuit
    import numpy as np
    
    # Create a balanced oracle (e.g., f(x) = x0 XOR x1 for n=2)
    n = 2
    qc = QuantumCircuit(n + 1)
    # Use CNOT gates to implement f(x) = x0 XOR x1 on the last qubit
    qc.cx(0, n)
    qc.cx(1, n)
    
    result = candidate(qc)
    assert result is False, "Balanced oracle should return False"