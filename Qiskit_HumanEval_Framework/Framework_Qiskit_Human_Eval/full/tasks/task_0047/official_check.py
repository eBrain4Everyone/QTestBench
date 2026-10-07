def check(candidate):
    samples = 2000
    result = candidate(samples)

    assert result.keys() == {'Heads', 'Tails'}
    assert round(result['Heads']/samples, 1) == 0.5
    assert round(result['Tails']/samples, 1) == 0.5
