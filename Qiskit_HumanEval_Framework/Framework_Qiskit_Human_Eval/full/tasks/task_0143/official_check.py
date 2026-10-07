def check(candidate):
    can_list = candidate()
    assert len(can_list) == 10, "Length of returned list is not 10"
    for _, item in enumerate(can_list):
        assert isinstance(item[0], Statevector)
        assert isinstance(item[1], Statevector)
        assert(state_fidelity(item[0], item[1]))>=0.9, "State fidelity of the returned pairs is less than 0.9"
