def check(candidate):
    assert candidate(10, 20) == {"00011110": 1024}
    assert candidate(61, 9) == {"00110100": 1024}
    assert candidate(47, 8) == {"00100111": 1024}
