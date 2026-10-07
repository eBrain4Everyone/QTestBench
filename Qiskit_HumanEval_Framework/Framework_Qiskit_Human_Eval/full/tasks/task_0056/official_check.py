def check(candidate):
    assert candidate(0) == {"11111111": 1024}
    assert candidate(238) == {"00010001": 1024}
    assert candidate(59) == {"11000100": 1024}
