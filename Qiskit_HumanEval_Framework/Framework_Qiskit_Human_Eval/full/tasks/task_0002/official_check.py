def check(candidate):
    result = candidate()
    solution = (Statevector.from_label("00") + Statevector.from_label("11")) / sqrt(2)
    assert result.equiv(solution)
