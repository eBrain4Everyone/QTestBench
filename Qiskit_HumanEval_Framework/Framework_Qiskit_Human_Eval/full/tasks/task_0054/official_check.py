def check(candidate):
    assert candidate(1, 2) == {'000': 1024}
    assert candidate(6, 7) == {'110': 1024}
    assert candidate(3, 5) == {'001': 1024}
