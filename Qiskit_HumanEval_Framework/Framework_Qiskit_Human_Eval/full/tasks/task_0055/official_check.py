def check(candidate):
    assert candidate(1, 2) == {"011": 1024}
    assert candidate(6, 7) == {"111": 1024}
    assert candidate(0, 5) == {"101": 1024}
