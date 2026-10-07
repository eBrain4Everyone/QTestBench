def check(candidate):
    from matplotlib.figure import Figure
    result = candidate()
    assert type(result) == Figure
    assert len(result.axes) == 5
    assert result.get_suptitle() == "fake_belem Error Map"
