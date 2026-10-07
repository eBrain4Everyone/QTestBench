def check(candidate):
    from qiskit.circuit.library import LinearFunction
    full, limited = candidate()
    full_linear_count = sum(1 for instr in full.data if isinstance(instr.operation, LinearFunction))
    limited_linear_count = sum(1 for instr in limited.data if isinstance(instr.operation, LinearFunction))
    assert full_linear_count == 1
    assert limited_linear_count > 1
