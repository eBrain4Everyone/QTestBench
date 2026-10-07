def check(candidate):
    stab, probabilities_dict = candidate()
    assert isinstance(stab, StabilizerState)
    assert isinstance(probabilities_dict, dict)
    assert probabilities_dict == {"00": 0.5, "11": 0.5}
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    new_stab = StabilizerState(qc)
    assert stab.equiv(new_stab)
