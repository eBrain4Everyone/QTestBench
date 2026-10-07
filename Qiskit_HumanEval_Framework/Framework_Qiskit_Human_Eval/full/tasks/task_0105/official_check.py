def check(candidate):
    result = candidate()
    assert isinstance(result, CNOTDihedral), f'Expected result to be CNOTDihedral, but got {type(result)}'
    assert result.linear.tolist() == [[1, 0], [1, 1]]
    assert str(result.poly) == "0 + x_0"
    assert result.shift.tolist() == [0, 0]
