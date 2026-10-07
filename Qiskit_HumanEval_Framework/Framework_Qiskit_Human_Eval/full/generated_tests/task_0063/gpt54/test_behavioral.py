# BEHAVIORAL tests — Qiskit HumanEval task task_0063
# Generated: 2026-04-28T12:38:35.787888
# Model: openai/gpt-5.4 (gpt54)
# Framework: Qiskit HE (isolated from QHack)

# --- Official check block start (injected) ---
OFFICIAL_CHECK_SOURCE = 'def check(candidate):\n    from numpy.random import seed\n    seed(12345)\n    basis = [1, 0, 0, 1, 1]\n    circuit = QuantumCircuit(5)\n    circuit.x([3, 4])\n    circuit.h([0, 3, 4])\n    result = candidate(basis, circuit)\n    assert result == "1"\n'
ENTRY_POINT_NAME = 'bb84_circuit_generate_key'
# --- Official check block end ---
def test_matching_z_basis_key_1():
    import builtins as _b
    from qiskit import QuantumCircuit
    import numpy as np

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    senders_basis = [0, 0, 0, 0]
    circuit = QuantumCircuit(4, 4)
    circuit.x(0)
    circuit.x(2)
    circuit.measure(range(4), range(4))

    key = candidate(senders_basis, circuit)

    assert isinstance(key, str), "The function must return the generated key as a string."
    assert key == "1010", f"For matching Z-basis preparation/measurement, expected key '1010', got {key!r}."
    assert set(key).issubset({"0", "1"}), "The returned key must contain only binary characters."


def test_matching_x_basis_key_2():
    import builtins as _b
    from qiskit import QuantumCircuit

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    senders_basis = [1, 1, 1]
    circuit = QuantumCircuit(3, 3)
    circuit.h(0)
    circuit.x(1)
    circuit.h(1)
    circuit.measure(range(3), range(3))

    key = candidate(senders_basis, circuit)

    assert isinstance(key, str), "The function must return a string key for X-basis inputs as well."
    assert key == "110", f"For deterministic X-basis states |+>, |->, |0>, expected key '110', got {key!r}."
    assert len(key) == len(senders_basis), "When all sender bases are provided, the produced key length should match the number of qubits."


def test_mixed_basis_filters_and_order_3():
    import builtins as _b
    from qiskit import QuantumCircuit

    sol = _b.INJECTED_SOLUTION_CODE
    entry = _b.INJECTED_ENTRY_POINT
    g = {"__builtins__": __builtins__}
    exec(sol, g)
    candidate = g[entry]

    senders_basis = [0, 1, 0, 1]
    circuit = QuantumCircuit(4, 4)
    circuit.x(0)
    circuit.h(1)
    circuit.x(2)
    circuit.h(3)
    circuit.measure(range(4), range(4))

    key = candidate(senders_basis, circuit)

    assert isinstance(key, str), "The generated BB84 key must be returned as a string."
    assert key == "1011", f"For a mixed-basis circuit with deterministic prepared states, expected key '1011', got {key!r}."
    assert len(key) == 4, "The key should preserve one bit per provided sender basis entry in the original qubit order."