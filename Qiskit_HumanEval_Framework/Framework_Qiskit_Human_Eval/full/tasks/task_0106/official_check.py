def check(candidate):
    result = candidate()
    assert isinstance(result, CNOTDihedral), f'Expected result to be CNOTDihedral, but got {type(result)}'
    assert result.linear.tolist() == [[1, 0], [0, 1]]
    assert str(result.poly) == "0 + 2*x_0"
    assert list(result.shift) == [0, 1]
