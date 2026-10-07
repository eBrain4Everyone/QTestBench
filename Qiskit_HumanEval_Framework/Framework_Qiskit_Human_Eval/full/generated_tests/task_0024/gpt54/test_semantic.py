# SEMANTIC tests — Qiskit HumanEval task task_0024
# Generated: 2026-04-28T12:36:18.671823
# Model: openai/gpt-5.4 (gpt54)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    balanced = QuantumCircuit(5)\n    balanced.cx(3, 4)\n    assert candidate(balanced) == False\n    constant = QuantumCircuit(9)\n    constant.x(8)\n    assert candidate(constant) == True\n'
ENTRY_POINT_NAME = 'dj_algorithm'
# --- Official check block end ---
def test_constant_zero_oracle_1():
    import builtins as _b
    import numpy as np
    from qiskit import QuantumCircuit

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    oracle = QuantumCircuit(2)
    result = candidate(oracle)

    assert isinstance(result, bool), "dj_algorithm should return a bool for a valid oracle."
    assert result is True, "Deutsch-Jozsa should classify an always-zero oracle as constant (True)."


def test_constant_one_oracle_2():
    import builtins as _b
    import numpy as np
    from qiskit import QuantumCircuit

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    oracle = QuantumCircuit(3)
    oracle.x(2)

    result = candidate(oracle)

    assert isinstance(result, bool), "dj_algorithm should return a bool for a valid oracle."
    assert result is True, "Deutsch-Jozsa should classify an always-one oracle as constant (True)."


def test_balanced_parity_oracle_3():
    import builtins as _b
    import numpy as np
    from qiskit import QuantumCircuit

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    oracle = QuantumCircuit(3)
    oracle.cx(0, 2)
    oracle.cx(1, 2)

    result = candidate(oracle)

    assert isinstance(result, bool), "dj_algorithm should return a bool for a valid oracle."
    assert result is False, "Deutsch-Jozsa should classify a balanced parity oracle as non-constant (False)."