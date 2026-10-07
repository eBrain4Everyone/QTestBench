def check(candidate):
    from math import sqrt
    from qiskit.quantum_info import state_fidelity
    desired_vector = [0.25j, 1 /sqrt(8)+0j, 0.25+0.25j, 0, 0,1 / sqrt(8) * (1+2j), 0.25+0j, 0]
    result = candidate(desired_vector)
    assert isinstance(result, dict)
    assert result == {"101": 665, "010": 118, "000": 49, "110": 51, "001": 141}
