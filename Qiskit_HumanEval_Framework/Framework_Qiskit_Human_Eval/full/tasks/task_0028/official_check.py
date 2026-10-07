def check(candidate):
    from matplotlib.patches import Rectangle
    result = candidate()
    assert isinstance(result, Figure)
    gca = result.gca()
    assert {xlabel.get_text() for xlabel in gca.get_xticklabels()} == {"00", "11"}
    objs = gca.findobj(Rectangle)
    assert len(objs) >= 4
    counts = [obj.get_height() for obj in objs[:4]]
    shots = counts[0] + counts[1]
    for i in range(4):
        assert round(counts[i]/shots, 1) == 0.5
