def check(candidate):
    from qiskit.quantum_info import state_fidelity
    from math import sqrt
    assert round(state_fidelity(candidate(1), [1/sqrt(2)]*2),3)==1
    assert round(state_fidelity(candidate(2), [0.5]*4),3)==1
    assert round(state_fidelity(candidate(3), [1/sqrt(8)]*8),3)==1
