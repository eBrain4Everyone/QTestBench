def check(candidate):
    result = candidate()
    assert isinstance(result, ScalarOp), f'Expected result to be ScalarOp, but got {type(result)}'
    assert result.coeff == 4
    assert result.input_dims() == (2,)
